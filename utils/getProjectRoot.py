from pathlib import Path


def find_project_root(current_path: Path, marker_file: str):
    for parent in current_path.parents:
        if (parent / marker_file).exists():
            return parent
    return current_path

