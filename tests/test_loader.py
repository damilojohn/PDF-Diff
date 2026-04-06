"""
Tests for loader.py — extract_pages() and render_pages()
"""
import pytest
import tempfile
from pathlib import Path
from PIL import Image
from pdf_diff.loader import extract_pages, render_pages


def _write_temp_pdf(pdf_bytes: bytes) -> Path:
    """Write PDF bytes to a temp file and return the path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.write(pdf_bytes)
    tmp.close()
    return Path(tmp.name)


class TestExtractPages:
    def test_returns_list(self, identical_pdf_bytes):
        pdf_a, _ = identical_pdf_bytes
        path = _write_temp_pdf(pdf_a)
        result = extract_pages(path)
        assert isinstance(result, list)

    def test_page_count_matches(self, identical_pdf_bytes):
        pdf_a, _ = identical_pdf_bytes
        path = _write_temp_pdf(pdf_a)
        result = extract_pages(path)
        assert len(result) == 3

    def test_returns_strings(self, identical_pdf_bytes):
        pdf_a, _ = identical_pdf_bytes
        path = _write_temp_pdf(pdf_a)
        result = extract_pages(path)
        assert all(isinstance(p, str) for p in result)

    def test_empty_page_returns_empty_string(self):
        import fitz
        doc = fitz.open()
        doc.new_page()  # blank page, no text
        path = _write_temp_pdf(doc.tobytes())
        result = extract_pages(path)
        assert result == [""]


class TestRenderPages:
    def test_returns_list(self, identical_pdf_bytes):
        pdf_a, _ = identical_pdf_bytes
        path = _write_temp_pdf(pdf_a)
        result = render_pages(path)
        assert isinstance(result, list)

    def test_page_count_matches(self, identical_pdf_bytes):
        pdf_a, _ = identical_pdf_bytes
        path = _write_temp_pdf(pdf_a)
        result = render_pages(path)
        assert len(result) == 3

    def test_returns_pil_images(self, identical_pdf_bytes):
        pdf_a, _ = identical_pdf_bytes
        path = _write_temp_pdf(pdf_a)
        result = render_pages(path)
        assert all(isinstance(img, Image.Image) for img in result)

    def test_images_have_positive_dimensions(self, identical_pdf_bytes):
        pdf_a, _ = identical_pdf_bytes
        path = _write_temp_pdf(pdf_a)
        result = render_pages(path)
        for img in result:
            width, height = img.size
            assert width > 0 and height > 0

    def test_dpi_affects_image_size(self, single_page_pdf_bytes):
        pdf, _ = single_page_pdf_bytes
        path = _write_temp_pdf(pdf)
        low_dpi = render_pages(path, dpi=72)
        high_dpi = render_pages(path, dpi=150)
        assert high_dpi[0].size > low_dpi[0].size
