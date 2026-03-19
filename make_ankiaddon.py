import os
import zipfile
from datetime import datetime
from pathlib import Path

from bump import increment_patch, read_current_version
from new_version import sync_version

# Configuration
ADDON_NAME = "Review_Hotmouse_Plus_Overview"
ADDON_DIR = "addon"

def artifact_names(
    addon_name: str,
    version: str,
    when: datetime | None = None,
) -> tuple[str, str]:
    dt = when or datetime.today()
    timestamp = dt.strftime("%Y%m%d%H%M")
    base = f"{addon_name}_v{version}_{timestamp}"
    return f"{base}.zip", f"{base}.ankiaddon"

def bump_version():
    try:
        addon_path = Path(ADDON_DIR)
        current_version = read_current_version(addon_path)
        new_version = increment_patch(current_version)
        print(f"Bumping version: {current_version} → {new_version}")
        sync_version(new_version, addon_path)
    except Exception as e:
        print(f"Warning: Could not auto-bump version: {e}")

def create_ankiaddon():
    # Auto-bump version before building
    bump_version()
    
    # Get the project root and addon directory
    root_dir = Path.cwd()
    addon_path = root_dir / ADDON_DIR
    
    if not addon_path.exists():
        print(f"Error: {ADDON_DIR} directory not found.")
        return

    try:
        current_version = read_current_version(addon_path)
    except Exception as e:
        print(f"Error: Could not determine current version: {e}")
        return

    zip_name, final_name = artifact_names(ADDON_NAME, current_version)

    # Exclusions
    exclude_dirs = ['__pycache__', '.git', '.vscode', '.github', 'tests']
    exclude_exts = ['.ankiaddon', '.pyc']
    exclude_files = ['meta.json', '.gitignore', '.gitmodules', 'mypy.ini']

    print(f"Creating {final_name} from {ADDON_DIR}...")

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the addon directory specifically
        for root, dirs, files in os.walk(addon_path):
            # Filter directories in-place
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = Path(root) / file
                # Skip excluded files/extensions
                if file in exclude_files or file_path.suffix in exclude_exts:
                    continue
                
                # Calculate the path relative to the 'addon/' folder 
                # so that __init__.py is at the root of the zip
                archive_name = file_path.relative_to(addon_path)
                zipf.write(file_path, archive_name)

    # Rename to .ankiaddon
    if os.path.exists(final_name):
        os.remove(final_name)
    os.rename(zip_name, final_name)
    print(f"Successfully created: {final_name}")

if __name__ == "__main__":
    create_ankiaddon()
