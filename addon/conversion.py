import re


def convert_text(txt: str) -> str:
    out = re.sub(r"\$\$([\s\S]*?)\$\$", r"\\[\1\\]", txt, flags=re.DOTALL)
    out = re.sub(r"\$([\s\S]*?)\$", r"\\(\1\\)", out, flags=re.DOTALL)
    return out
