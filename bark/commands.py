import sys
from datetime import datetime

import requests

from bark.db import DatabaseManager

db = DatabaseManager('../bookmarks.db')


"""
1) получить начальную страницу результатов со звездами (конечная
точка: https://api.github.com/users/{github_username}/starred);
2) разобрать данные из отклика, чтобы выполнить команду
AddBookmarkCommand для каждого помеченного звездой репозитория;
3) получить заголовок Link: <…>; rel=next, если он есть;
4) повторить
"""


class ImportGitHubStarsCommand:
    """Class to process adding GitHub starts into bookmarks"""

    @staticmethod
    def _extract_bookmark_info(repo: dict) -> dict:
        """
        Method returns dict with repo data
        """

        return {
            'title': repo.get('name'),
            'url': repo.get('html_url'),
            'notes': repo.get('description')
        }

    def execute_stars_import(self, data: dict) -> str:
        """
        Method processing starts import to bookmarks
        """

        bookmarks_imported = 0
        github_username = data.get('github_username')
        next_page = f'https://api.github.com/users/{github_username}/starred'
        while next_page:
            stars_response = requests.get(
                next_page, headers={
                    "Accept": "application/vnd.github.v3.start+json"
                }
            )
            next_page = stars_response.links.get('next', {}).get('url')

            for repo_info in stars_response.json():
                repo = repo_info.get('repo')

                if data.get('preserve_timestamps'):
                    timestamp = datetime.strptime(
                        repo_info['starred_at'], '%Y-%m-%dT%H:%M:%SZ'
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand.execute(
                    self._extract_bookmark_info(repo), timestamp=timestamp
                )

        return f'Imported {bookmarks_imported} bookmarks from github stars!'


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
    def execute(data: dict, timestamp=None) -> str:
        """
        Method creates bookmark in db
        :param data: dict -> bookmark data
        :param timestamp: timestamp -> timestamp of creation
        :return: str -> response text
        """
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
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


class UpdateBookmarkCommand:
    """Class to update bookmark"""

    @staticmethod
    def execute(bookmark_id: int | str, data: dict) -> str:
        """
        Method to update bookmark by id
        :param bookmark_id: int -> bookmark id
        :param data: dict -> bookmark data
        :return: str -> response text
        """

        db.update('bookmarks', bookmark_id, data)
        return "Bookmark updated!"


class QuitCommand:
    """Class to quit the program"""

    @staticmethod
    def execute() -> None:
        """
        Method to run quit command
        :return: None
        """

        sys.exit()
