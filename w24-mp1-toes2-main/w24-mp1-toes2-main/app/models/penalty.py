from .codable import Codable


class Penalty(Codable):
    def __init__(self, pid: int, bid: int, amount: int, paidAmount: int) -> None:
        assert type(pid) is int

        self.id = pid
        self.borrowID = bid
        self.fee = amount
        self.paid = paidAmount

    @property
    def amountLeft(self):
        return self.fee - self.paid

    @staticmethod
    def createFrom(data: dict):
        return Penalty(data["pid"], data["bid"], data["amount"], data["paid_amount"])

    @property
    def table(self) -> str:
        return "penalties"

    @property
    def columns(self) -> tuple:
        return ("bid", "amount", "paid_amount")

    @property
    def values(self):
        return (self.borrowID, self.fee, self.paid)
