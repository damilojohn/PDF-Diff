# pdf-diff

A command-line tool to compare two PDF files page by page and report which pages have changed.

## Installation

### Windows

1. Open **PowerShell** (search for it in the Start menu)
2. Run the following command:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

> If you downloaded this as a zip, extract it first and run the command from inside the extracted folder.

### macOS / Linux

1. Open **Terminal**
2. Run the following command:

```sh
sh install.sh
```

Both scripts will automatically install [uv](https://docs.astral.sh/uv/) (a Python package manager) if you don't have it, then install `pdf-diff`.

---

## Usage

```
pdf-diff <pdf_a> <pdf_b> [--threshold 0-1] [--output FILE]
```

### Examples

Compare two PDFs and print the results:
```sh
pdf-diff original.pdf revised.pdf
```

Use a looser threshold (flag pages that are less than 80% similar):
```sh
pdf-diff original.pdf revised.pdf --threshold 0.80
```

Save the report to a text file:
```sh
pdf-diff original.pdf revised.pdf --output report.txt
```

### Options

| Option | Default | Description |
|---|---|---|
| `--threshold` | `0.95` | Similarity ratio (0–1) below which a page is flagged as different |
| `--output` | stdout | Write the report to a file instead of printing it |

### Example output

```
Comparing: original.pdf (10 pages) vs revised.pdf (12 pages)

DIFFERENT pages:
  Page    3  — similarity: 72.4%
  Page    7  — similarity: 88.1%
  Page   11  — only in revised.pdf
  Page   12  — only in revised.pdf

Summary: 2 changed, 2 added, 0 removed, 8 identical
```

---

## Development

Requires [uv](https://docs.astral.sh/uv/).

```sh
# Clone the repo
git clone https://github.com/damilojohn/PDF-Diff.git
cd PDF-Diff

# Install dependencies and the tool in editable mode
uv pip install -e .

# Run directly
uv run pdf-diff doc_a.pdf doc_b.pdf
```
