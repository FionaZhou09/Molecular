from pathlib import Path


def test_project_skeleton_files_exist():
    project_root = Path(__file__).resolve().parents[1]

    expected_paths = [
        "README.md",
        "requirements.txt",
        "src/__init__.py",
        "data/raw/.gitkeep",
        "data/processed/.gitkeep",
        "results/figures/.gitkeep",
        "notebooks/.gitkeep",
        "tests/.gitkeep",
    ]

    for relative_path in expected_paths:
        assert (project_root / relative_path).exists()


def test_src_package_imports():
    __import__("src")
