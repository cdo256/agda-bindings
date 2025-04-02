# Agda → Obsidian Typing Bindings Converter

**Type in [Obsidian](https://obsidian.md/) the same way you type in Agda.**  
This tool generates rules for [obsidian-latex-suite](https://github.com/artempyanykh/obsidian-latex-suite) from Agda’s Unicode input method, allowing seamless LaTeX-style math input in Obsidian using familiar Agda-style sequences like `->`, `\bN`, `\all`, etc.

## What It Does

- Extracts Agda's Unicode input bindings.
- Converts each Unicode character into LaTeX using `pylatexenc`.
- Outputs snippet-like rules for obsidian-latex-suite that work in both text and math modes.

Example output:

```json
{trigger: "\\bN", replacement: "\\mathbb{N}", options: "mA"},
{trigger: "\\bN", replacement: "$\\mathbb{N}$", options: "tA"},
```

## Why?

Agda users are used to typing rich Unicode math notation directly using escape sequences. With this tool, you can bring the same typing experience into Obsidian for taking notes, writing papers, or documenting proofs.

## Current Limitations

⚠️ This is a **very basic first version**, and it has several known limitations:

- **No handling of superscripts, subscripts, or suffix-based variants.**
- **No disambiguation for many visually identical sequences.**
- **Many Unicode characters are not mapped to LaTeX and are inserted as-is**, which may not render correctly or be the canonical LaTeX representation.
- Sequences containing quotes (`"`) are skipped to avoid CSV escaping issues.

**Pull requests welcome!**  
If you’d like to improve the mappings, add better formatting logic, or handle more edge cases—please contribute!

## Project Structure

- **`extract-bindings.el`** – Elisp script that extracts Unicode bindings from Agda and writes them to `bindings.csv`.
- **`convert-bindings.py`** – Python script that:
  - Calls `just-agda` to run the extraction.
  - Converts Unicode characters to LaTeX using `pylatexenc`.
  - Outputs obsidian-latex-suite-compatible JSON-style rules.
- **`flake.nix` + `flake.lock`** – Nix-based development environment for reproducibility.

## How to Use

### Prerequisites

This setup currently relies on [Nix](https://nixos.org/) flakes so you need Nix with flakes enabled to get it to work. That should set up all the dependencies and work without an issue. This however means that Windows and any other operating system without Nix will require manual setup to work.

Nix will install Emacs via my custom wrapper [just-agda](https://github.com/cdo256/just-agda) which is simply a Nix flake which generates with just enough to run Agda in Emacs.

If instead you want/have to set this up manually, you will need:

- Python 3 with `pylatexenc` 2.10 or newer
- Emacs - tested on 30.2 but should work on other versions
- Agda - At least 2.2.0 (must be compatible with Emacs)
- `agda-mode` installed on Emacs

Regardless of whether you use Nix, you will need:

- [Obsidian](https://obsidian.md/)
- [Obsidian Latex Suite](https://github.com/artisticat1/obsidian-latex-suite)

### Steps

1. Enter the development shell:
   ```bash
   nix develop
   ```
2. Run the script:
   ```bash
   python convert-bindings.py > <YOUR_OBSIDIAN_DIRECTORY>/latex-suite-snippets.json
   ```
3. In Obsidian > Settings > Community Plugins > Latex Suite, set the folder location to point to the JSON file you just created.

This will:

- Extract Unicode bindings using Agda + Elisp.
- Convert them into LaTeX.
- Output rules formatted for obsidian-latex-suite.
- Set up Obsidian to replace these keystrokes as you type.

## License

Free and open source under then MIT License.
