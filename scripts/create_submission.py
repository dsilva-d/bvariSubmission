from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "submission"
EXCLUDED_PARTS = {
    ".DS_Store",
    ".venv",
    "__pycache__",
    "node_modules",
    "submission",
}
EXCLUDED_FILENAMES = {
    "Software Developer Technical Exercise.docx",
    "Software Developer Technical Exercise.pdf",
}
EXCLUDED_SUFFIXES = {
    ".pyc",
}


def should_include(path: Path) -> bool:
    relative = path.relative_to(ROOT_DIR)

    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False

    if path.name in EXCLUDED_FILENAMES:
        return False

    if path.suffix in EXCLUDED_SUFFIXES:
        return False

    return path.is_file()


def create_submission(first_name: str, last_name: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)

    clean_first = "".join(first_name.split())
    clean_last = "".join(last_name.split())
    output_path = (
        OUTPUT_DIR
        / f"Software_Developer_Exercise_2026-{clean_last}{clean_first}.txt"
    )

    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT_DIR.rglob("*")):
            if should_include(path):
                archive.write(path, path.relative_to(ROOT_DIR))

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create the renamed zip submission file for the exercise."
    )
    parser.add_argument("--first-name", required=True)
    parser.add_argument("--last-name", required=True)
    args = parser.parse_args()

    output_path = create_submission(args.first_name, args.last_name)
    print(f"Created submission file: {output_path}")


if __name__ == "__main__":
    main()
