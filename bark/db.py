import sqlite3


class DatabaseManager:
    def __init__(self, db_path: str):
        """
        Method initializes path to db
        :param db_path: str -> path to db
        """

        self.connection = sqlite3.connect(db_path)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values=None):
        """
        Method to execute data
        :param statement: str -> statement for execution
        :return: sqlite cursor
        """

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: dict):
        """
        Method creates table in db
        :param table_name: str -> table name
        :param columns: dict -> key=column name, value=data type
        :return: None
        """

        columns = tuple(
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        )
        self._execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
        )

    def add(self, table_name: str, columns: dict):
        """
        Method creates row in table
        :param table_name: str -> table name to create row in
        :param columns: dict -> columns to insert values in
        :return: None
        """

        placeholders = ", ".join('?' * len(columns))
        column_names = ", ".join(columns.keys())
        column_values = tuple(columns.values())
        self._execute(
            f"INSERT INTO {table_name} ({column_names})"
            f"VALUES ({placeholders});", column_values
        )

    def update(self, table_name: str, obj_id: int | str, columns: dict):
        """
        Method updates row in table
        :param table_name: str -> table name to create row in
        :param obj_id: str or int -> obj id to update
        :param columns: dict -> columns to update with criteria
        :return: None
        """

        placeholders = tuple(f'{column} = ?' for column in columns.keys())
        update_criteria = ' AND '.join(placeholders)
        self._execute(
            f"UPDATE {table_name} SET {update_criteria} WHERE id={obj_id};",
            tuple(columns.values())
        )

    def delete(self, table_name: str, columns: dict):
        """
        Method deletes row from table
        :param table_name: str -> table name
        :param columns: dict -> columns to delete with criteria
        :return: None
        """

        placeholders = tuple(f'{column} = ?' for column in columns.keys())
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f"DELETE FROM {table_name} WHERE {delete_criteria};",
            tuple(columns.values())
        )

    def select(self, table_name: str, columns: dict = None,
               order_by: str = None):
        """
        Method select rows from table
        :param table_name: str -> table name
        :param columns: dict -> columns to filter by
        :param order_by: str -> column to order by
        :return: None
        """

        criteria = columns or {}
        query = f"SELECT * FROM {table_name}"
        if criteria:
            placeholders = tuple(
                f"{column} = ?" for column in columns.keys()
            )
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        if order_by:
            query += f" ORDER BY {order_by}"

        return self._execute(query, tuple(columns.values()))
