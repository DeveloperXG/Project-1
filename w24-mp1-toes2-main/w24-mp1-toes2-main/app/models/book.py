from .codable import Codable
from enum import IntEnum


class BookStatus(IntEnum):
    Available = 0
    Borrowed = 1


class Book(Codable):
    def __init__(self, bookID: int, title: str, author: str,
                 publishedYear: int, averageRating: float,
                 bookStatus: BookStatus) -> None:
        assert type(bookID) is int

        self.id = bookID
        self.title = title
        self.author = author
        self.publishedYear = publishedYear
        # Extra fields
        self.avgRating = averageRating
        self.borrowed = (bookStatus == BookStatus.Borrowed)

    @staticmethod
    def createFrom(data: dict):
        return Book(data["book_id"], data["title"], data["author"], data["pyear"],
                    data["avg_rating"], BookStatus(int(data["status"])))

    @property
    def table(self) -> str:
        return "books"

    @property
    def columns(self) -> tuple:
        return ("title", "author", "pyear")

    @property
    def values(self) -> tuple:
        return (self.title, self.author, self.publishedYear)
