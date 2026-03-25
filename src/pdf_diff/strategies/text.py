from .base import DiffStrategy
import difflib


class TextDiff(DiffStrategy):

    def compare_pages(pages_a: list[str], pages_b: list[str], threshold: float):
        """Compare two pdfs text contents using SequenceMatcher.
        """
        shared = min(len(pages_a), len(pages_b))
        len_a, len_b = len(pages_a), len(pages_b)
        identical = 0
        different = []

        for i in range(shared):
            similarity_ratio = difflib.SequenceMatcher(None,
                                                       pages_a[i],
                                                       pages_b[i]).ratio()

            if similarity_ratio < threshold:
                different.append(i + 1, similarity_ratio)
            else:
                identical += 1

        if len_a == len_b:
            added = []
            removed = []
        else:
            added = list(range(shared + 1, len_b + 1))
            removed = list(range(shared + 1, len_a + 1))

        return {
            "added": added,
            "removed": removed,
            "changed": different,
            "identical": identical,
            "len_a": len_a,
            "len_b": len_b
        }
