"""
Provides common database retrieval methods.
Builds on db.py
"""

from .db import DB
from .models.member import Member
from .models.borrowing import Borrowing
from .models.penalty import Penalty
from .models.book import Book
from collections import namedtuple


class Query():
    BorrowingCounts = namedtuple("BorrowingCounts",
                                 "total, returned, unreturned, overdue")

    def __init__(self, database: DB) -> None:
        assert isinstance(database, DB)

        self._db = database

    def userExists(self, email: str) -> bool:
        assert isinstance(email, str)

        query = "SELECT COUNT(*) FROM members WHERE LOWER(email)=?"
        value = self._db.getSingleValue(query, (email.lower(),))

        return (int(value) == 1)

    def checkLogin(self, email: str, password: str) -> bool:
        assert isinstance(email, str) and isinstance(password, str)

        query = "SELECT COUNT(*) FROM members WHERE LOWER(email)=? AND passwd=?"
        value = self._db.getSingleValue(query, (email.lower(), password))

        return (int(value) == 1)

    def getMember(self, email: str) -> Member:
        assert isinstance(email, str)

        query = "SELECT * FROM members WHERE email=?"
        data = self._db.retrieve(query, (email,))
        if data is not None:
            return Member.createFrom(data[0])

        raise Exception("query.getMember(): Member does not exist")

    def getBorrowing(self, bid: int) -> Borrowing:
        assert type(bid) is int

        query = "SELECT * FROM borrowings JOIN books USING(book_id) WHERE bid=?"
        data = self._db.retrieve(query, (bid,))
        if data is not None:
            return Borrowing.createFrom(data[0])
        else:
            raise Exception("query.getBorrowing(): Error")

    def getBookTitle(self, bookID: int) -> str:
        assert type(bookID) is int

        query = "SELECT title FROM books WHERE book_id=?;"
        data = self._db.getSingleValue(query, (bookID,))
        return data

    def getBorrowCounts(self, member: str) -> BorrowingCounts:
        assert isinstance(member, str)

        total = returned = unreturned = overdue = 0

        totalAndReturnedBorrowingsQ = """
            SELECT COUNT(*) AS total, COUNT(end_date) as returned
            FROM borrowings WHERE member=?;
            """
        totalAndReturnedData = self._db.retrieve(totalAndReturnedBorrowingsQ,
                                                 (member,))
        if totalAndReturnedData is not None:
            total = int(totalAndReturnedData[0]["total"])
            returned = int(totalAndReturnedData[0]["returned"])
            unreturned = total - returned

        overdueQ = """SELECT COUNT(*) FROM borrowings
            WHERE end_date IS NULL
            AND julianday('now') > (julianday(start_date)+20)
            AND member=?;
            """
        value = self._db.getSingleValue(overdueQ, (member,))
        if value is not None:
            overdue = value

        return self.BorrowingCounts(total, returned, unreturned, overdue)

    def getDebt(self, member: str) -> int:
        assert isinstance(member, str)

        query = """SELECT COALESCE(SUM(amount - paid_amount), 0)
            FROM penalties JOIN borrowings USING(bid)
            WHERE member=?;
            """
        value = self._db.getSingleValue(query, (member,))
        if value is not None:
            return value
        else:
            raise Exception("query.getDebt(): Member does not exist")

    def getCurrentBorrowings(self, member: str) -> list:
        assert isinstance(member, str)

        query = """ SELECT * FROM borrowings
            JOIN books USING(book_id)
            WHERE member=? AND end_date IS NULL;
            """

        data = self._db.retrieve(query, (member,))
        if data is not None:
            return [Borrowing.createFrom(d) for d in data]
        else:
            raise Exception("query.getBorrowings(): Database Error")

    def getUnpaidPenalties(self, member: str) -> list:
        assert isinstance(member, str)

        query = """SELECT pid, penalties.bid, amount, COALESCE(paid_amount, 0) as paid_amount
            FROM penalties JOIN borrowings USING(bid)
            WHERE amount > COALESCE(paid_amount, 0) AND member=?;
            """
        data = self._db.retrieve(query, (member,))
        if data is not None:
            return [Penalty.createFrom(d) for d in data]
        else:
            raise Exception("query.getPenalties(): Database Error")

    def search(self, text: str, limit: int) -> list:
        assert type(text) is str
        assert type(limit) is int

        query = """SELECT books.book_id, title, author, pyear,
                    IFNULL(round(AVG(rating), 1), 0) as avg_rating,
                    (COUNT(borrowedBooks.book_id) != 0) as status
            FROM books
            LEFT JOIN reviews USING(book_id)
            LEFT JOIN
                (SELECT DISTINCT book_id FROM borrowings WHERE end_date IS NULL) AS borrowedBooks
            USING(book_id)
            WHERE title LIKE :text OR author LIKE :text
            GROUP BY books.book_id
            ORDER BY
                CASE
                    WHEN title LIKE :text THEN 1
                    ELSE 2
                END,
                title COLLATE NOCASE,
                author COLLATE NOCASE
            LIMIT :limit;
            """

        data = self._db.retrieve(
            query, {"text": f"%{text}%", "limit": limit})
        if data is not None:
            return [Book.createFrom(d) for d in data]
        return []
