from abc import ABC, abstractmethod


class DiffStrategy(ABC):
    @abstractmethod
    def compare_pages(pages_a: list, pages_b: list) -> float:
        """Compare page sequences and returns a similarity ration"""
