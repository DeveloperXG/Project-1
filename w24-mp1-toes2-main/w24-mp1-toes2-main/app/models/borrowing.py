from .codable import Codable
from datetime import date, timedelta


class Borrowing(Codable):
    def __init__(self, bid, member: str, bookID: int, bookTitle: str,
                 startDate: date, endDate: date) -> None:
        self.id = bid
        self.borrower = member
        self.bookID = bookID
        self.bookTitle = bookTitle  # Extra field
        self.borrowDate = startDate
        self.returnedDate = endDate

    @property
    def dueDate(self):
        # `startDate` + 20 days
        return self.borrowDate + timedelta(days=20)

    @staticmethod
    def createFrom(data: dict):
        return Borrowing(data["bid"], data["member"], data["book_id"],
                         data["title"], data["start_date"], data["end_date"])

    @property
    def table(self) -> str:
        return "borrowings"

    @property
    def columns(self) -> tuple:
        return ("member", "book_id", "start_date", "end_date")

    @property
    def values(self) -> tuple:
        return (self.borrower, self.bookID, self.borrowDate, self.returnedDate)
