from .strategies import text, image
from .strategies.base import DiffStrategy


def compare_pages(
        pages_a: list,
        pages_b: list,
        strategy: DiffStrategy,
        threshold: float = 0.95
) -> dict:
    """Compares pdf pages based on the selected strategy, returns a dict containing the comparison report"""
    if strategy == text.TextDiff:
        results = text.TextDiff.compare_pages(
            pages_a,
            pages_b,
            threshold
        )
        return results

    if strategy == image.ImageDiff:
        # use the image diff library
        pass
