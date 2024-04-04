from .codable import Codable


class Member(Codable):
    def __init__(self, email: str, passwd: str, name: str,
                 birthYear: int, faculty: str) -> None:
        assert type(email) is str

        self.email = email
        self.passwd = passwd
        self.name = name
        self.birthYear = birthYear
        self.faculty = faculty

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Member):
            return self.email == __value.email and\
                self.passwd == __value.passwd and\
                self.name == __value.name and\
                self.birthYear == __value.birthYear and\
                self.faculty == __value.faculty
        return False

    @staticmethod
    def createFrom(data: dict):
        return Member(data["email"], data["passwd"],
                      data["name"], data["byear"],
                      data["faculty"])

    @property
    def table(self) -> str:
        return "members"

    @property
    def columns(self) -> tuple:
        return ("email", "passwd", "name", "byear", "faculty")

    @property
    def values(self) -> tuple:
        return (self.email, self.passwd, self.name, self.birthYear, self.faculty)
