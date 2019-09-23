"""
The UseDatabase context manager for working with MySQL.

Simple example usage:

    from db_cm import UseDatabase, SQLError

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


class ConnectionError(Exception):
    pass


class CredentialsError(Exception):
    pass


class SQLError(Exception):
    pass


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
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> 'None':
        """ Tidy up connection after commiting changes.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
