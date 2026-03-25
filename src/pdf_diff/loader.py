from pathlib import Path
import pdfplumber


def extract_pages(pdf_path: Path) -> list[str]:
    """Return a list of text strings, one per page."""
    with pdfplumber.open(pdf_path) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]