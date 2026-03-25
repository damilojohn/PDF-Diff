import argparse
import sys
from pathlib import Path
from .loader import extract_pages
from .comparer import compare_pages
from .reporter import format_report
from .strategies import text, image


def main():
    parser = argparse.ArgumentParser(
        prog="pdf-diff",
        description="Compare two PDF files page by page and report differences.",
    )
    parser.add_argument("pdf_a", type=Path, help="First (original) PDF")
    parser.add_argument("pdf_b", type=Path, help="Second (modified) PDF")
    parser.add_argument(
      "--strategy",
      choices=["text", "image", "hybrid"],
      default="text",
  )
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

    STRATEGIES = {
      "text": text.TextDiff,
      "image": image.ImageDiff,
      }
    strategy = STRATEGIES[args.strategy]

    results = compare_pages(pages_a, pages_b, strategy, args.threshold)
    report = format_report(args.pdf_a, args.pdf_b, results)

    if args.output:
        args.output.write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
