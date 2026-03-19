import importlib.util
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONVERSION_PATH = PROJECT_ROOT / "addon" / "conversion.py"
_spec = importlib.util.spec_from_file_location("addon_conversion", CONVERSION_PATH)
_module = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_module)
convert_text = _module.convert_text


class DelimiterConversionTests(unittest.TestCase):
    def test_inline_math_conversion(self) -> None:
        self.assertEqual(convert_text("$x+y$"), r"\(x+y\)")

    def test_display_math_conversion(self) -> None:
        self.assertEqual(convert_text("$$x^2$$"), r"\[x^2\]")

    def test_mixed_inline_and_display_conversion(self) -> None:
        self.assertEqual(
            convert_text("a $x$ b $$y$$ c"),
            r"a \(x\) b \[y\] c",
        )

    def test_multiline_display_math_conversion(self) -> None:
        self.assertEqual(
            convert_text("$$x\n+ y$$"),
            "\\[x\n+ y\\]",
        )

    def test_text_without_dollar_delimiters_is_unchanged(self) -> None:
        src = r"\(x\) and \[y\]"
        self.assertEqual(convert_text(src), src)

    def test_converts_multiple_segments(self) -> None:
        self.assertEqual(
            convert_text("$a$ $b$ $$c$$"),
            r"\(a\) \(b\) \[c\]",
        )


if __name__ == "__main__":
    unittest.main()
