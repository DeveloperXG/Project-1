from .codable import Codable
from datetime import date


class Review(Codable):
    def __init__(self, rid, bookID: int, member: str,
                 rating: int, text: str) -> None:
        self.id = rid
        self.bookID = bookID
        self.writer = member
        self.ratingNo = rating
        self.text = text
        self.dateWritten = date.today()

    @staticmethod
    def createFrom(data: dict):
        return Review(data["rid"], data["book_id"],
                      data["member"], data["rating"],
                      data["rtext"], data["rdate"])

    @property
    def table(self) -> tuple:
        return "reviews"

    @property
    def columns(self) -> tuple:
        return ("book_id", "member", "rating", "rtext", "rdate")

    @property
    def values(self):
        return (self.bookID, self.writer, self.ratingNo, self.text, self.dateWritten)
