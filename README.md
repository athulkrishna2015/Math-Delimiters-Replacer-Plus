# [Math Delimiters Replacer Plus](https://github.com/athulkrishna2015/Math-Delimiters-Replacer-Plus)
[Install via ankiweb](https://ankiweb.net/shared/info/699086701)

This add-on converts MathJax delimiters while editing notes and when batch-updating selected cards in the Browser, using the same matching logic as the original project it builds on 
(Supports Bulk update)

## What it does 
- Replace display math: `$$ … $$` → `\[ … \]` without altering the inner TeX content 
- Replace inline math: `$ … $` → `\( … \)` with the same guarantees as above 
- Adds a toolbar button labelled `\(...\)` in the Editor for one‑click conversion of the current selection  
- Adds a Browser action named `\(...\)` that processes all fields of all selected notes, with a single undo group for Ctrl+Z  

![giphy](https://github.com/user-attachments/assets/68712ef8-ad94-4503-b8d2-8f6c384fbcb8)


## Installation 
- Install from AnkiWeb by opening Tools → Add‑ons → Get Add‑ons and entering the code 401047458 for the maintained “Math Delimiters Replacer LaTeX MathJax – Fixed by Shige,” or visit its AnkiWeb page for details 
- For historical reference and behavior parity, see the original “Math Delimiters Replacer – LaTeX, MathJax” entry on AnkiWeb under code 211799575 

## Usage 
- Editor: select text containing `$…$` or `$$…$$`, then click the `\(...\)` toolbar button or press the configured shortcut to convert delimiters in place in the active field 
- Browser: select any cards, open the Edit menu, choose `\(...\)`, and the add‑on will convert delimiters in every field of the selected notes with one undo checkpoint for the whole run 

## Keyboard shortcut 
- The shortcut is read from `config.json` key `"hotkey"` and is applied to both the Editor action and the Browser menu action on startup 
- If a plain Alt+letter collides with menu mnemonics on your platform, set `"hotkey"` to a combination like `Shift+Alt+M` in `config.json` and reload add‑ons to take effect 

## Compatibility 
- Tested on Anki 25 with Qt 6, with Browser and Editor integrations registered through modern hooks and with fallbacks for older APIs where practical 
- Undo is implemented with `start_undo/stop_undo` when available and falls back to a checkpoint on older collections to preserve a single-step revert 

## Notes on MathJax delimiters 
- Anki’s manual documents MathJax inline `\(...\)` and display `\[...\]` delimiters, which this add‑on standardizes from `$` and `$$` sources used in some notes 
- For equations that include backslashes or non‑breaking spaces, insertion uses a safe transport so the literal `\[`/`\(` sequences appear as intended in the field text before rendering 

## Attribution and credits 
- Original concept and regex logic credited to the “[Math Delimiters Replacer – LaTeX, MathJax](https://github.com/achyutmorang/math-delimiters-replacer-addon)” add‑on by Achyut Morang (AnkiWeb code [211799575](https://ankiweb.net/shared/info/211799575)) 
- This maintained version adapts it for modern Anki releases and adds Browser batch processing and a text‑label toolbar button, published as “[Math Delimiters Replacer LaTeX MathJax – Fixed by Shige](https://www.reddit.com/r/Anki/comments/1b0eybn/simple_fix_of_broken_addons_for_the_latest_anki/)” (AnkiWeb code [401047458](https://ankiweb.net/shared/info/401047458)) 

## Support and source pointers 
- For usage instructions, updates, and issue reporting, consult the maintained add‑on’s AnkiWeb page under code 401047458 
- For background, screenshots, and original documentation, refer to the legacy add‑on page under code 211799575 
