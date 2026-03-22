import json
import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import bump
import make_ankiaddon


def _write_manifest(path: Path, version: str, human_version: str | None = None) -> None:
    manifest = {
        "package": "math_delimiters_replacer",
        "name": "Math Delimiters Replacer",
        "version": version,
    }
    if human_version is not None:
        manifest["human_version"] = human_version
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


@contextmanager
def _working_directory(path: Path):
    original = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original)


def _write_addon_fixture(addon_dir: Path, version: str) -> None:
    addon_dir.mkdir(parents=True, exist_ok=True)
    _write_manifest(addon_dir / "manifest.json", version=version, human_version=version)
    (addon_dir / "VERSION").write_text(f"{version}\n", encoding="utf-8")
    (addon_dir / "__init__.py").write_text("# test addon fixture\n", encoding="utf-8")


class VersioningTests(unittest.TestCase):
    def test_validate_version_requires_major_minor_patch(self) -> None:
        self.assertEqual(bump.validate_version("1.2.3"), "1.2.3")
        for bad in ("1.2", "1", "v1.2.3", "1.2.3.4", "1.2.x"):
            with self.assertRaises(ValueError):
                bump.validate_version(bad)

    def test_sync_version_updates_manifest_and_version_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            addon_dir = Path(tmp) / "addon"
            addon_dir.mkdir(parents=True, exist_ok=True)
            _write_manifest(addon_dir / "manifest.json", version="0.1.0")

            bump.sync_version("2.4.6", addon_dir)

            manifest = json.loads((addon_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["version"], "2.4.6")
            self.assertEqual(manifest["human_version"], "2.4.6")
            self.assertEqual((addon_dir / "VERSION").read_text(encoding="utf-8").strip(), "2.4.6")

    def test_read_current_version_prefers_version_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            addon_dir = Path(tmp) / "addon"
            addon_dir.mkdir(parents=True, exist_ok=True)
            _write_manifest(addon_dir / "manifest.json", version="0.1.0", human_version="0.1.0")
            (addon_dir / "VERSION").write_text("3.3.7\n", encoding="utf-8")

            self.assertEqual(bump.read_current_version(addon_dir), "3.3.7")

    def test_read_current_version_falls_back_to_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            addon_dir = Path(tmp) / "addon"
            addon_dir.mkdir(parents=True, exist_ok=True)
            _write_manifest(addon_dir / "manifest.json", version="4.0.1")

            self.assertEqual(bump.read_current_version(addon_dir), "4.0.1")

    def test_bump_version_increments_patch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            addon_dir = Path(tmp) / "addon"
            addon_dir.mkdir(parents=True, exist_ok=True)
            _write_manifest(addon_dir / "manifest.json", version="1.2.3")
            (addon_dir / "VERSION").write_text("1.2.3\n", encoding="utf-8")

            self.assertEqual(bump.bump_version(addon_dir), 0)

            manifest = json.loads((addon_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["version"], "1.2.4")
            self.assertEqual(manifest["human_version"], "1.2.4")
            self.assertEqual((addon_dir / "VERSION").read_text(encoding="utf-8").strip(), "1.2.4")

    def test_make_ankiaddon_bump_version_uses_semver_patch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            addon_dir = Path(tmp) / "addon"
            addon_dir.mkdir(parents=True, exist_ok=True)
            _write_manifest(addon_dir / "manifest.json", version="9.1.2")
            (addon_dir / "VERSION").write_text("9.1.2\n", encoding="utf-8")

            old_addon_dir = make_ankiaddon.ADDON_DIR
            try:
                make_ankiaddon.ADDON_DIR = str(addon_dir)
                self.assertEqual(make_ankiaddon.bump_version(), 0)
            finally:
                make_ankiaddon.ADDON_DIR = old_addon_dir

            manifest = json.loads((addon_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["version"], "9.1.3")
            self.assertEqual((addon_dir / "VERSION").read_text(encoding="utf-8").strip(), "9.1.3")

    def test_create_ankiaddon_without_explicit_version_bumps_patch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            addon_dir = root / "addon"
            _write_addon_fixture(addon_dir, "1.2.3")

            old_addon_dir = make_ankiaddon.ADDON_DIR
            try:
                make_ankiaddon.ADDON_DIR = "addon"
                with _working_directory(root):
                    self.assertEqual(make_ankiaddon.create_ankiaddon(), 0)

                manifest = json.loads((addon_dir / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["version"], "1.2.4")
                self.assertEqual((addon_dir / "VERSION").read_text(encoding="utf-8").strip(), "1.2.4")

                built = list(root.glob("Math_delimiters_replacer_plus_v1.2.4_*.ankiaddon"))
                self.assertEqual(len(built), 1)
            finally:
                make_ankiaddon.ADDON_DIR = old_addon_dir

    def test_create_ankiaddon_with_explicit_version_does_not_bump(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            addon_dir = root / "addon"
            _write_addon_fixture(addon_dir, "5.0.7")

            old_addon_dir = make_ankiaddon.ADDON_DIR
            try:
                make_ankiaddon.ADDON_DIR = "addon"
                with _working_directory(root):
                    self.assertEqual(make_ankiaddon.create_ankiaddon("5.2.0"), 0)

                manifest = json.loads((addon_dir / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["version"], "5.2.0")
                self.assertEqual((addon_dir / "VERSION").read_text(encoding="utf-8").strip(), "5.2.0")

                built = list(root.glob("Math_delimiters_replacer_plus_v5.2.0_*.ankiaddon"))
                self.assertEqual(len(built), 1)
            finally:
                make_ankiaddon.ADDON_DIR = old_addon_dir

    def test_artifact_name_includes_version(self) -> None:
        when = datetime(2026, 3, 19, 12, 30)
        zip_name, addon_name = make_ankiaddon.artifact_names("MyAddon", "1.4.0", when)
        self.assertEqual(zip_name, "MyAddon_v1.4.0_202603191230.zip")
        self.assertEqual(addon_name, "MyAddon_v1.4.0_202603191230.ankiaddon")


if __name__ == "__main__":
    unittest.main()
