# -*- coding: utf-8 -*-
"""
Math Delimiters Replacer
- replace $$...$$ -> \[...\] and $...$ -> \(...\)
(Anki 25 / Qt6 compatible; regex lines UNCHANGED)
"""
from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from anki.hooks import addHook
from aqt.editor import Editor
import re, json

# Try modern hooks (present in Anki 25)
try:
    from aqt import gui_hooks
    HAS_GUI_HOOKS = True
except Exception:
    HAS_GUI_HOOKS = False

# ----- config helpers -----
def get_key():
    conf = mw.addonManager.getConfig(__name__)
    return conf.get("hotkey", "") if conf else ""

def format_key(k):
    return QKeySequence(k).toString(QKeySequence.SequenceFormat.NativeText)

# ----- regex logic (UNCHANGED) -----
def _convert_text(txt: str) -> str:
    out = re.sub(r"\$\$([\s\S]*?)\$\$", r"\\[\1\\]", txt, flags=re.DOTALL)
    out = re.sub(r"\$([\s\S]*?)\$", r"\\(\1\\)", out, flags=re.DOTALL)
    return out

# ----- editor: replace current selection via toolbar button/hotkey -----
def replaceMathDelimiters(editor: Editor):
    web = editor.web
    selected_text = web.selectedText()
    modified = _convert_text(selected_text)  # regex untouched
    # Insert as literal text; JSON keeps backslashes and NBSP intact
    web.page().runJavaScript(
        f"document.execCommand('insertText', false, {json.dumps(modified)});"
    )

def setupEditorButtonsFilter(buttons, editor: Editor):
    key = get_key()
    btn = editor.addButton(
        None,
        "replaceMathDelimiters",
        replaceMathDelimiters,
        tip=f"Replace Math Delimiters ({format_key(key)})",
        keys=key,
        label=r"\(...\)",  # text button; no icon asset required
    )
    buttons.append(btn)
    return buttons

addHook("setupEditorButtons", setupEditorButtonsFilter)

# Also bind the hotkey via the editor's shortcut table to avoid menu mnemonic conflicts.
def _editor_shortcuts(shortcuts, editor):
    key = get_key()
    if key:
        shortcuts.append((key, lambda: replaceMathDelimiters(editor)))

if HAS_GUI_HOOKS:
    gui_hooks.editor_did_init_shortcuts.append(_editor_shortcuts)

# ----- browser: batch process selected notes with undo -----
def _start_undo():
    try:
        mw.col.start_undo()
        return "new"
    except Exception:
        mw.checkpoint("Replace Math Delimiters")
        return "old"

def _stop_undo(kind):
    if kind == "new":
        try:
            mw.col.stop_undo("Replace Math Delimiters")
        except Exception:
            pass

def _get_note(nid):
    try:
        return mw.col.get_note(nid)  # newer API
    except Exception:
        return mw.col.getNote(nid)   # older API

def _save_note(note):
    for fn in (getattr(note, "flush", None),
               getattr(mw.col, "update_note", None),
               getattr(note, "save", None)):
        try:
            if fn:
                fn(note) if fn is getattr(mw.col, "update_note", None) else fn()
                return
        except Exception:
            continue

def replace_in_browser(browser):
    undo_kind = _start_undo()
    nids = browser.selectedNotes()
    changed = 0
    for nid in nids:
        note = _get_note(nid)
        touched = False
        for fld in note.keys():
            orig = note[fld]
            new = _convert_text(orig)  # regex untouched
            if new != orig:
                note[fld] = new
                touched = True
        if touched:
            _save_note(note)
            changed += 1
    _stop_undo(undo_kind)
    try:
        browser.model.reset()
    except Exception:
        try:
            mw.reset()
        except Exception:
            pass
    tooltip(f"Replaced math delimiters in {changed} notes.")

def _set_widget_with_children_context(act: QAction):
    # PyQt6: use enum class; PyQt5: legacy attribute
    try:
        act.setShortcutContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)  # PyQt6
    except Exception:
        try:
            act.setShortcutContext(Qt.WidgetWithChildrenShortcut)              # PyQt5
        except Exception:
            pass

def _add_browser_action(browser):
    key = get_key()
    act = QAction(r"\(...\)", browser)
    if key:
        act.setShortcut(QKeySequence(key))
        _set_widget_with_children_context(act)
    act.setToolTip(f"Replace Math Delimiters in selected notes ({format_key(key)})")
    act.triggered.connect(lambda: replace_in_browser(browser))
    # Add to Edit menu across versions
    try:
        browser.form.menuEdit.addAction(act)      # newer
    except Exception:
        try:
            browser.form.menu_edit.addAction(act) # older
        except Exception:
            browser.addAction(act)

if HAS_GUI_HOOKS:
    gui_hooks.browser_menus_did_init.append(_add_browser_action)
else:
    addHook("browser.setupMenus", _add_browser_action)
