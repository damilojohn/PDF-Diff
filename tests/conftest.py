"""
Shared pytest fixtures — builds minimal in-memory PDFs using PyMuPDF
so tests have no dependency on external files.
"""
import pytest
import fitz  # PyMuPDF
from PIL import Image


def _make_pdf(texts: list[str]) -> bytes:
    """Create a PDF in memory with one page per text entry."""
    doc = fitz.open()
    for text in texts:
        page = doc.new_page(width=595, height=842)  # A4
        page.insert_text((72, 72), text, fontsize=14)
    return doc.tobytes()


# --- PDF bytes fixtures ---

@pytest.fixture
def identical_pdf_bytes():
    """Two PDFs with exactly the same content."""
    content = ["Page one content", "Page two content", "Page three content"]
    return _make_pdf(content), _make_pdf(content)


@pytest.fixture
def different_pdf_bytes():
    """Two PDFs where every page has completely different text."""
    pdf_a = _make_pdf(["Alpha page one", "Alpha page two"])
    pdf_b = _make_pdf(["Zzzzzz totally different", "Zzzzzz totally different"])
    return pdf_a, pdf_b


@pytest.fixture
def mismatched_pdf_bytes():
    """PDF A has 2 pages, PDF B has 4 pages."""
    pdf_a = _make_pdf(["Shared page one", "Shared page two"])
    pdf_b = _make_pdf(["Shared page one", "Shared page two", "Extra page three", "Extra page four"])
    return pdf_a, pdf_b


@pytest.fixture
def single_page_pdf_bytes():
    """Two single-page PDFs — one identical pair, one different pair."""
    same = _make_pdf(["Same content"])
    different = _make_pdf(["Completely different xyz"])
    return same, different


# --- PIL Image fixtures (for testing ImageDiff directly without PDF rendering) ---

@pytest.fixture
def white_image():
    return Image.new("RGB", (595, 842), color=(255, 255, 255))


@pytest.fixture
def black_image():
    return Image.new("RGB", (595, 842), color=(0, 0, 0))


@pytest.fixture
def identical_image_pages(white_image):
    """Two lists of identical PIL images."""
    return [white_image, white_image], [white_image, white_image]


@pytest.fixture
def different_image_pages(white_image, black_image):
    """Two lists of maximally different PIL images."""
    return [white_image, white_image], [black_image, black_image]
