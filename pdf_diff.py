"""
pdf_diff.py — CLI tool to compare two PDFs page by page and report differences.
"""

import argparse
import difflib
import sys
from pathlib import Path

import pdfplumber


def extract_pages(pdf_path: Path) -> list[str]:
    """Return a list of text strings, one per page."""
    with pdfplumber.open(pdf_path) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]


def compare_pages(
    pages_a: list[str],
    pages_b: list[str],
    threshold: float,
) -> dict:
    """
    Compare pages positionally.
    Returns a result dict with changed, added, removed, and identical counts.
    """
    len_a, len_b = len(pages_a), len(pages_b)
    shared = min(len_a, len_b)

    changed = []
    identical = 0

    for i in range(shared):
        ratio = difflib.SequenceMatcher(None, pages_a[i], pages_b[i]).ratio()
        if ratio < threshold:
            changed.append((i + 1, ratio))  # 1-indexed page number
        else:
            identical += 1

    added = list(range(shared + 1, len_b + 1))    # pages only in B
    removed = list(range(shared + 1, len_a + 1))  # pages only in A

    return {
        "changed": changed,
        "added": added,
        "removed": removed,
        "identical": identical,
        "len_a": len_a,
        "len_b": len_b,
    }


def format_report(path_a: Path, path_b: Path, results: dict) -> str:
    lines = []
    lines.append(
        f"\nComparing: {path_a.name} ({results['len_a']} pages)"
        f" vs {path_b.name} ({results['len_b']} pages)\n"
    )

    has_diffs = results["changed"] or results["added"] or results["removed"]

    if not has_diffs:
        lines.append("No differences found. All pages are identical.\n")
    else:
        lines.append("DIFFERENT pages:")
        for page_num, ratio in results["changed"]:
            lines.append(f"  Page {page_num:>4}  — similarity: {ratio * 100:.1f}%")
        for page_num in results["removed"]:
            lines.append(f"  Page {page_num:>4}  — only in {path_a.name}")
        for page_num in results["added"]:
            lines.append(f"  Page {page_num:>4}  — only in {path_b.name}")
        lines.append("")

    lines.append(
        f"Summary: {len(results['changed'])} changed, "
        f"{len(results['added'])} added, "
        f"{len(results['removed'])} removed, "
        f"{results['identical']} identical"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        prog="pdf-diff",
        description="Compare two PDF files page by page and report differences.",
    )
    parser.add_argument("pdf_a", type=Path, help="First (original) PDF")
    parser.add_argument("pdf_b", type=Path, help="Second (modified) PDF")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.95,
        metavar="0-1",
        help="Similarity ratio below which a page is considered different (default: 0.95)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        metavar="FILE",
        help="Write report to a text file instead of stdout",
    )
    args = parser.parse_args()

    for p in (args.pdf_a, args.pdf_b):
        if not p.exists():
            print(f"Error: file not found — {p}", file=sys.stderr)
            sys.exit(1)
        if p.suffix.lower() != ".pdf":
            print(f"Error: not a PDF file — {p}", file=sys.stderr)
            sys.exit(1)

    if not 0.0 <= args.threshold <= 1.0:
        print("Error: --threshold must be between 0 and 1", file=sys.stderr)
        sys.exit(1)

    pages_a = extract_pages(args.pdf_a)
    pages_b = extract_pages(args.pdf_b)

    results = compare_pages(pages_a, pages_b, args.threshold)
    report = format_report(args.pdf_a, args.pdf_b, results)

    if args.output:
        args.output.write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
