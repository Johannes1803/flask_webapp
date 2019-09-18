"""
The UseDatabase context manager for working with MySQL.

Simple example usage:

    from DBcm import UseDatabase, SQLError

    config = { 'host': '127.0.0.1',
               'user': 'myUserid',
               'password': 'myPassword',
               'database': 'myDB' }

    with UseDatabase(config) as cursor:
        _SQL = "select * from log"
        cursor.execute(_SQL)
        data = cursor.fetchall()

Requires Python 3.
"""

import mysql.connector


class UseDatabase:
    def __init__(self, config: dict):
        """ Add the database config parameters to the object.

        On Object creation, pass a dictionary with all relevant
        information on the connection to MySQL.
        Minimum required key-value pairs:
        host -- ip address of host running MySQL
        user -- the MySQL username
        password -- of the user
        database -- name of database
        """
        self.configuration = config

    def __enter__(self) -> 'cursor':
        """ Establish connection to mySQL.

        On established connection return a cursor object.
        """
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> 'None':
        """ Tidy up connection after commiting changes.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
