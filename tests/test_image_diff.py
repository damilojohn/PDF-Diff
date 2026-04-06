"""
Tests for ImageDiff.compare_pages()
"""
import pytest
from PIL import Image
from pdf_diff.strategies.image import ImageDiff


class TestImageDiffIdenticalPages:
    def test_identical_pages_return_similarity_one(self, identical_image_pages):
        pages_a, pages_b = identical_image_pages
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        assert result["identical"] == 2
        assert result["changed"] == []

    def test_identical_pages_no_added_or_removed(self, identical_image_pages):
        pages_a, pages_b = identical_image_pages
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        assert result["added"] == []
        assert result["removed"] == []


class TestImageDiffDifferentPages:
    def test_different_pages_are_flagged(self, different_image_pages):
        pages_a, pages_b = different_image_pages
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        assert len(result["changed"]) == 2

    def test_changed_pages_are_1_indexed(self, different_image_pages):
        pages_a, pages_b = different_image_pages
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        page_numbers = [p for p, _ in result["changed"]]
        assert page_numbers == [1, 2]

    def test_changed_entry_contains_similarity_ratio(self, different_image_pages):
        pages_a, pages_b = different_image_pages
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        for _, ratio in result["changed"]:
            assert 0.0 <= ratio <= 1.0

    def test_similarity_ratio_below_threshold(self, different_image_pages):
        pages_a, pages_b = different_image_pages
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        for _, ratio in result["changed"]:
            assert ratio < 0.95


class TestImageDiffPageMismatch:
    def test_extra_pages_in_b_are_added(self, white_image, black_image):
        pages_a = [white_image]
        pages_b = [white_image, black_image, black_image]
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        assert result["added"] == [2, 3]
        assert result["removed"] == []

    def test_extra_pages_in_a_are_removed(self, white_image, black_image):
        pages_a = [white_image, black_image, black_image]
        pages_b = [white_image]
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        assert result["removed"] == [2, 3]
        assert result["added"] == []


class TestImageDiffReturnStructure:
    def test_result_has_required_keys(self, identical_image_pages):
        pages_a, pages_b = identical_image_pages
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        assert set(result.keys()) == {"changed", "added", "removed", "identical", "len_a", "len_b"}

    def test_len_a_and_len_b_are_correct(self, white_image, black_image):
        pages_a = [white_image, white_image]
        pages_b = [black_image, black_image, black_image]
        result = ImageDiff.compare_pages(pages_a, pages_b, threshold=0.95)
        assert result["len_a"] == 2
        assert result["len_b"] == 3
