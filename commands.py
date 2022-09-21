import sys
from datetime import datetime

from db import DatabaseManager
from python_pro.bark.bark import Option

db = DatabaseManager('bookmarks.db')


class CreateBookmarksTableCommand:
    """Class creates table in db"""

    @staticmethod
    def execute() -> None:
        """
        Method executes creation of table in db
        :return: None
        """

        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })


class AddBookmarkCommand:
    """Class adds bookmark to db"""

    @staticmethod
    def add_bookmark(data: dict) -> str:
        """
        Method creates bookmark in db
        :param data: dict -> bookmark data
        :return: str -> response text
        """
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return "Bookmark successfully added!"


class ListBookmarksCommand:
    """Class lists bookmarks"""

    def __init__(self, order_by: str = 'date_added'):
        self.order_by = order_by

    def execute(self) -> list:
        """
        Method to get bookmarks
        :return: list -> data list
        """

        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    """Class to delete bookmark"""

    @staticmethod
    def execute(bookmark_id: int or str) -> str:
        """
        Method to delete bookmark by id
        :param bookmark_id: int -> bookmark id
        :return: str -> response text
        """

        db.delete('bookmarks', {'id': bookmark_id})
        return "Bookmark deleted!"


class QuitCommand:
    """Class to quit the program"""

    @staticmethod
    def execute() -> None:
        """
        Method to run quit command
        :return: None
        """

        sys.exit()
