import json
import re
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

    version_path = addon_root / "VERSION"
    version_path.write_text(f"{version_string}\n", encoding="utf-8")

def increment_patch(version_string: str) -> str:
    try:
        major, minor, patch = map(int, version_string.split("."))
    except ValueError as e:
        raise ValueError(
            f"Invalid version '{version_string}'. Expected major.minor.patch"
        ) from e
    return f"{major}.{minor}.{patch + 1}"

def read_current_version(addon_dir: Path) -> str:
    version_file = addon_dir / "VERSION"
    if version_file.exists():
        version = version_file.read_text(encoding="utf-8").strip()
        return validate_version(version)

    manifest_file = addon_dir / "manifest.json"
    if manifest_file.exists():
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        for key in ("human_version", "version"):
            value = str(manifest.get(key, "")).strip()
            if value:
                try:
                    return validate_version(value)
                except ValueError:
                    continue

    raise FileNotFoundError(
        f"Could not determine current version from {version_file} or {manifest_file}"
    )

def bump_version(addon_dir: Path = Path("addon")) -> int:
    try:
        current_version = read_current_version(addon_dir)
        new_version = increment_patch(current_version)
        print(f"Bumping version: {current_version} → {new_version}")
        sync_version(new_version, addon_dir)
        print(f"Successfully updated manifest.json and VERSION to {new_version}")
        return 0
    except Exception as e:
        print(f"Failed to bump version: {e}")
        return 1

if __name__ == "__main__":
    raise SystemExit(bump_version())
