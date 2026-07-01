import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdFingerprintGenerator, rdMolDescriptors


DESCRIPTOR_COLUMNS = [
    "molecular_weight",
    "exact_molecular_weight",
    "heavy_atom_count",
    "atom_count",
    "logp",
    "tpsa",
    "h_bond_donors",
    "h_bond_acceptors",
    "rotatable_bonds",
    "ring_count",
    "aromatic_ring_count",
    "aliphatic_ring_count",
    "saturated_ring_count",
    "heteroatom_count",
    "formal_charge",
    "fraction_csp3",
    "molar_refractivity",
    "num_valence_electrons",
    "num_radical_electrons",
    "labute_asa",
    "balaban_j",
    "bertz_ct",
    "qed",
]

SUPPORTED_FINGERPRINT_BITS = {512, 1024, 2048}
DEFAULT_FINGERPRINT_BITS = 2048


def _mol_from_smiles(smiles: str, index: int) -> Chem.Mol:
    if not isinstance(smiles, str):
        raise ValueError(f"Invalid SMILES at index {index}: {smiles!r}")

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES at index {index}: {smiles!r}")
    return mol


def _descriptor_row(mol: Chem.Mol) -> dict[str, float]:
    return {
        "molecular_weight": Descriptors.MolWt(mol),
        "exact_molecular_weight": Descriptors.ExactMolWt(mol),
        "heavy_atom_count": float(mol.GetNumHeavyAtoms()),
        "atom_count": float(mol.GetNumAtoms()),
        "logp": Crippen.MolLogP(mol),
        "tpsa": rdMolDescriptors.CalcTPSA(mol),
        "h_bond_donors": float(Lipinski.NumHDonors(mol)),
        "h_bond_acceptors": float(Lipinski.NumHAcceptors(mol)),
        "rotatable_bonds": float(Lipinski.NumRotatableBonds(mol)),
        "ring_count": float(rdMolDescriptors.CalcNumRings(mol)),
        "aromatic_ring_count": float(rdMolDescriptors.CalcNumAromaticRings(mol)),
        "aliphatic_ring_count": float(rdMolDescriptors.CalcNumAliphaticRings(mol)),
        "saturated_ring_count": float(rdMolDescriptors.CalcNumSaturatedRings(mol)),
        "heteroatom_count": float(rdMolDescriptors.CalcNumHeteroatoms(mol)),
        "formal_charge": float(Chem.GetFormalCharge(mol)),
        "fraction_csp3": rdMolDescriptors.CalcFractionCSP3(mol),
        "molar_refractivity": Crippen.MolMR(mol),
        "num_valence_electrons": float(Descriptors.NumValenceElectrons(mol)),
        "num_radical_electrons": float(Descriptors.NumRadicalElectrons(mol)),
        "labute_asa": rdMolDescriptors.CalcLabuteASA(mol),
        "balaban_j": Descriptors.BalabanJ(mol),
        "bertz_ct": Descriptors.BertzCT(mol),
        "qed": Descriptors.qed(mol),
    }


def compute_descriptors(smiles_list) -> pd.DataFrame:
    rows = []
    for index, smiles in enumerate(smiles_list):
        mol = _mol_from_smiles(smiles, index)
        rows.append(_descriptor_row(mol))

    return pd.DataFrame(rows, columns=DESCRIPTOR_COLUMNS)


def compute_morgan_fingerprints(
    smiles_list,
    radius: int = 2,
    n_bits: int = 2048,
) -> np.ndarray:
    if n_bits not in SUPPORTED_FINGERPRINT_BITS:
        supported = ", ".join(str(bits) for bits in sorted(SUPPORTED_FINGERPRINT_BITS))
        raise ValueError(f"n_bits must be one of: {supported}")

    generator = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
    fingerprints = []

    for index, smiles in enumerate(smiles_list):
        mol = _mol_from_smiles(smiles, index)
        fingerprint = generator.GetFingerprintAsNumPy(mol).astype(np.uint8)
        fingerprints.append(fingerprint)

    if not fingerprints:
        return np.empty((0, n_bits), dtype=np.uint8)

    return np.vstack(fingerprints)


def build_feature_matrix(df: pd.DataFrame, feature_type: str) -> tuple[np.ndarray, list[str]]:
    smiles_list = df["smiles"].tolist()

    if feature_type == "descriptors":
        descriptors = compute_descriptors(smiles_list)
        return descriptors.to_numpy(), list(descriptors.columns)

    if feature_type == "fingerprints":
        fingerprints = compute_morgan_fingerprints(
            smiles_list,
            n_bits=DEFAULT_FINGERPRINT_BITS,
        )
        feature_names = [
            f"morgan_{index}" for index in range(DEFAULT_FINGERPRINT_BITS)
        ]
        return fingerprints, feature_names

    if feature_type == "combined":
        descriptors = compute_descriptors(smiles_list)
        fingerprints = compute_morgan_fingerprints(
            smiles_list,
            n_bits=DEFAULT_FINGERPRINT_BITS,
        )
        features = np.hstack([descriptors.to_numpy(), fingerprints])
        feature_names = list(descriptors.columns) + [
            f"morgan_{index}" for index in range(DEFAULT_FINGERPRINT_BITS)
        ]
        return features, feature_names

    supported = "descriptors, fingerprints, combined"
    raise ValueError(f"Unsupported feature_type: {feature_type!r}. Supported: {supported}")
