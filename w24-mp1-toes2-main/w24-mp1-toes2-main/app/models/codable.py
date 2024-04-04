from abc import ABC, abstractmethod


class Codable(ABC):
    @staticmethod
    @abstractmethod
    def createFrom(data: dict):
        pass

    @property
    @abstractmethod
    def table(self) -> str:
        pass

    @property
    @abstractmethod
    def columns(self) -> tuple:
        pass

    # Implementations will return the value of their columns
    #  needed for an insertion in the same order as `columns()`
    @property
    @abstractmethod
    def values(self) -> tuple:
        pass
