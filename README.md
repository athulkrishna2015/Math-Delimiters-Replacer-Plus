# [Math Delimiters Replacer Plus](https://github.com/athulkrishna2015/Math-Delimiters-Replacer-Plus)
[Install via ankiweb](https://ankiweb.net/shared/info/699086701)

This add-on converts MathJax delimiters while editing notes, batch-updating selected notes in the Browser, and updating the current note from the Reviewer More menu, using the same matching logic as the original project it builds on 
(Supports Bulk update)

## What it does 
- Replace display math: `$$ … $$` → `\[ … \]` without altering the inner TeX content 
- Replace inline math: `$ … $` → `\( … \)` with the same guarantees as above 
- Adds a toolbar button labelled `\(...\)` in the Editor for one‑click conversion of the current selection  
- Adds a Browser action named `\(...\)` that processes all fields of all selected notes, with a single undo group for Ctrl+Z  
- Adds a Reviewer More-menu action named `\(...\)` that converts delimiters in the current review note
- In Editor selection and full-field modes, preserves existing HTML formatting (`<b>`, `<i>`, `<u>`, spans, etc.) and only rewrites delimiter text
- Skips already rendered MathJax nodes so rendered equations are not modified

![giphy](https://github.com/user-attachments/assets/68712ef8-ad94-4503-b8d2-8f6c384fbcb8)


## Installation 
- Install from AnkiWeb by opening Tools → Add‑ons → Get Add‑ons and entering the code 699086701 

## Usage 
- Editor: select text containing `$…$` or `$$…$$`, then click the `\(...\)` toolbar button or press the configured shortcut to convert delimiters in place in the active field 
- Browser: select any cards, open the Edit menu, choose `\(...\)`, and the add‑on will convert delimiters in every field of the selected notes with one undo entry for the whole run 
- Reviewer: while reviewing a card, open the **More** menu, choose `\(...\)`, and the add‑on will convert delimiters in the current note and refresh the reviewer view

## Editor behavior details
- The editor command rewrites affected text nodes in place (selection or full field) and does not flatten rich text formatting
- Full-field mode includes both "no selection, cursor in field" and "select all inside a single field" workflows
- Full-field replacement no longer propagates first-line formatting (for example bold or font size) to remaining lines
- Existing rendered MathJax (for example `anki-mathjax`/MathJax render containers) is intentionally ignored
- Editor replacement uses a native editable-command path so `Ctrl+Z` in the card editor restores previous delimiters
- Scope is delimiter normalization only: `$...$`/`$$...$$` to `\(...\)`/`\[...\]`

## Keyboard shortcut 
- The shortcut is read from `config.json` key `"hotkey"` and is applied to both the Editor action and the Browser menu action on startup 
- Reviewer integration is exposed in the More menu (no dedicated reviewer hotkey)
- If a plain Alt+letter collides with menu mnemonics on your platform, set `"hotkey"` to a combination like `Shift+Alt+M` in `config.json` and reload add‑ons to take effect 

## Compatibility 
- Tested on Anki 25 with Qt 6, with Browser/Editor integrations registered through modern hooks and with fallbacks for older APIs where practical 
- Reviewer menu integration uses the `reviewer_will_show_context_menu` hook when available
- Undo is supported for Browser/Reviewer actions on modern Anki, with compatibility fallbacks on older builds
- Editor undo for selection replacement is integrated with the editor’s own undo stack (`Ctrl+Z` in the field)

## Notes on MathJax delimiters 
- Anki’s manual documents MathJax inline `\(...\)` and display `\[...\]` delimiters, which this add‑on standardizes from `$` and `$$` sources used in some notes 
- For equations that include backslashes or non‑breaking spaces, insertion uses a safe transport so the literal `\[`/`\(` sequences appear as intended in the field text before rendering 

## Attribution and credits 
- Original concept and regex logic credited to the “[Math Delimiters Replacer – LaTeX, MathJax](https://github.com/achyutmorang/math-delimiters-replacer-addon)” add‑on by Achyut Morang (AnkiWeb code [211799575](https://ankiweb.net/shared/info/211799575)) 
- Forked version adapts it for modern Anki releases  published as “[Math Delimiters Replacer LaTeX MathJax – Fixed by Shige](https://www.reddit.com/r/Anki/comments/1b0eybn/simple_fix_of_broken_addons_for_the_latest_anki/)” (AnkiWeb code [401047458](https://ankiweb.net/shared/info/401047458)) 

## Support and source pointers 
- For usage instructions, updates, and issue reporting, consult the maintained add‑on’s AnkiWeb page under code 401047458 
- For background, screenshots, and original documentation, refer to the legacy add‑on page under code 211799575

Developer-oriented workflows and versioning commands are documented in `DEVELOPMENT.md`.

## Changelog
- 2026-03-22
  - Fixed editor full-field replacement so multi-line fields keep per-line formatting instead of inheriting first-line style
  - Updated full-field processing to avoid style bleed while still converting delimiters in place
  - Fixed full-field detection for "select all in field" (`Ctrl+A`) so it follows the same formatting-safe path
  - Consolidated version tooling by removing `new_version.py` and moving sync/validation helpers into `bump.py`
  - Updated build flow so `make_ankiaddon.py <version>` sets explicit version without bumping, while no-arg mode still auto-bumps
- 2026-03-19
  - Added Reviewer More-menu action to convert delimiters in the current review note
  - Fixed Browser/Reviewer replacement undo behavior on modern Anki by using custom undo entry merging
  - Fixed card editor replacement undo so `Ctrl+Z` restores previous delimiters after replace
- 2026-02-20
  - Added support for full-field replacement: if no text is selected, clicking the button now replaces all math delimiters in the currently focused field.
  - Maintained existing behavior where only the selected text is processed if a selection exists.
- 2026-02-18
  - Editor conversion now preserves existing rich text formatting (bold, italics, underline, spans, etc.)
  - Editor conversion now skips already rendered MathJax content
  - Delimiter normalization scope clarified: only `$...$` and `$$...$$` are converted to `\(...\)` and `\[...\]`
