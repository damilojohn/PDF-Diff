"""Compares pdf images using perceptual hashing"""
from .base import DiffStrategy


class ImageDiff(DiffStrategy):
    def compare_pages(
            pages_a: list,
            pages_b: list,
            threshold
    ):
        pass
