import re
import sys
import json
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")

def validate_version(version_string: str) -> str:
    if not VERSION_RE.fullmatch(version_string):
        raise ValueError(
            f"Invalid version '{version_string}'. Expected format: major.minor.patch"
        )
    return version_string

def sync_version(version_string: str, addon_root: Path) -> None:
    validate_version(version_string)
    if not addon_root.is_dir():
        raise FileNotFoundError(f"Addon directory not found: {addon_root}")

    manifest_path = addon_root / "manifest.json"
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["version"] = version_string
    manifest["human_version"] = version_string
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    # human_version may only refresh on install.
    # Keep VERSION in sync for local development/build scripts.
    version_path = addon_root / "VERSION"
    version_path.write_text(f"{version_string}\n", encoding="utf-8")

def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python new_version.py <major.minor.patch> <addon_dir>")
        return 1

    version_string = argv[1]
    addon_root = Path(argv[2])

    try:
        sync_version(version_string, addon_root)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    print(f"Updated version to {version_string} in {addon_root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
