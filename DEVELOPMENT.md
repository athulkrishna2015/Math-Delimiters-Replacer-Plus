# Math Delimiters Replacer Plus - Developer Notes

This repository contains the source for the **Math Delimiters Replacer Plus** Anki add-on.

## Project Structure

- `addon/`: Add-on package contents.
  - `main.py`: Entry point and Anki hook/menu integration.
  - `config_dialog.py`: Add-on configuration window.
  - `manifest.json`: Add-on metadata.
  - `VERSION`: Local development version file (semantic version string).
- `bump.py`: Version helpers (`validate_version`, `sync_version`) and patch bump (`x.y.z` -> `x.y.(z+1)`).
- `make_ankiaddon.py`: Creates `.ankiaddon`; auto-bumps patch only when no explicit version is provided.
- `tests/`: Automated tests (versioning workflow and helpers).

## Features Wired Into Anki

- Editor toolbar button: convert selected (or active field) math delimiters.
- Browser Edit menu action: batch-convert selected notes.
- Reviewer More menu action: convert delimiters in the current review note.

## Undo Behavior

- Browser and Reviewer actions use grouped undo on modern Anki (`add_custom_undo_entry` + `merge_undo_entries`).
- Editor replacement integrates with the editor field undo stack, so `Ctrl+Z` in the editor restores previous delimiters.
- Legacy undo/checkpoint paths are retained only as compatibility fallbacks for older Anki APIs.

## Versioning Scheme

Version format is strictly:

```text
major.minor.patch
```

Examples: `1.0.0`, `1.2.7`, `2.0.0`.

Behavior:

- `bump.py` validates semantic version format and syncs:
  - `manifest.json` keys: `version`, `human_version`
  - `addon/VERSION`
- `bump.py` can read current version and increment patch.
- `make_ankiaddon.py` behavior:
  - Without args: auto-bumps patch via `bump.py`, then packages.
  - With `<major.minor.patch>` arg: writes that version via `bump.py` sync helpers, then packages without bumping.

## Common Commands

Bump patch version:

```shell
python bump.py
```

Build `.ankiaddon` locally:

```shell
python make_ankiaddon.py
```

Build `.ankiaddon` with explicit version (no auto-bump):

```shell
python make_ankiaddon.py 1.5.0
```

Output naming format:

```text
<ADDON_NAME>_v<major.minor.patch>_<YYYYMMDDHHMM>.ankiaddon
```

Run tests:

```shell
python -m unittest discover -s tests -p "test_*.py"
```

## Local Testing With Symlink

Linux:

```shell
ln -s "$(pwd)/addon" ~/.local/share/Anki2/addons21/math_delimiters_replacer_plus_dev
```

Windows (PowerShell as admin):

```powershell
New-Item -ItemType SymbolicLink -Path "$env:APPDATA\Anki2\addons21\math_delimiters_replacer_plus_dev" -Target "$pwd\addon"
```
