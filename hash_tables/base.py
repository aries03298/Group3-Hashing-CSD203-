from abc import ABC, abstractmethod


class BaseHashTable(ABC):
    """Giao diện chung: put trả về số lượt dò; get trả về (giá trị, số lượt dò)."""

    @abstractmethod
    def put(self, key, value) -> int:
        ...

    @abstractmethod
    def get(self, key):
        ...
