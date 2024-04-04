"""
This module creates an interface for talking with the database.
query.py builds on this interface by encapsulating common operations
"""

import sqlite3
from .models.codable import Codable


class DB():

    def __init__(self, connection: sqlite3.Connection) -> None:
        assert isinstance(connection, sqlite3.Connection)

        self._connection = connection

    def getSingleValue(self, query: str, params: tuple) -> str:
        assert isinstance(query, str)
        assert isinstance(params, tuple)

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            value = cursor.fetchone()[0]

            return value
        except sqlite3.Error:
            return None

    def retrieve(self, query: str, params: tuple) -> list:
        assert isinstance(query, str)
        assert type(params) is tuple or type(params) is dict

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error:
            return None

    def insert(self, obj: Codable) -> bool:
        assert isinstance(obj, Codable)

        # INSERT INTO [table](col1, col2, ...) VALUES (?, ?, ...)
        insertionStatement = f"INSERT INTO {obj.table}(" + \
            ','.join(obj.columns) + ')'
        insertionStatement += " VALUES(" + \
            ','.join(['?'] * len(obj.values)) + ");"

        try:
            cursor = self._connection.cursor()
            cursor.execute(insertionStatement, obj.values)
            self._connection.commit()
            return True
        except sqlite3.Error:
            return False

    def updateColumn(self, column: str, value, increment: bool,
                     table: str, where: str,
                     whereParams: tuple) -> bool:
        assert type(column) is str and type(
            table) is str and type(where) is str
        assert value is not None
        assert type(whereParams) is tuple or whereParams is None

        if whereParams is None:
            whereParams = tuple()

        updateStatement = f"UPDATE {table} "
        updateStatement += f"SET {column}={(column + ' +') if increment else ''}? "
        updateStatement += f"WHERE {where};"

        try:
            cursor = self._connection.cursor()
            cursor.execute(updateStatement, (value,) + whereParams)
            self._connection.commit()
            return True
        except sqlite3.Error:
            return False
