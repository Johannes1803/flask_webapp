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
    """Raised if it is not possible to reach the database."""


class CredentialsError(Exception):
    """Raised if the database credentials are wrong."""


class SQLError(Exception):
    """Raised if the sql query contains errors."""


class UseDatabase:
    """Handle communication between the database MySql and custom python code.

        Implements the context management protocol for use in pythons
        'with' statement.
    """

    def __init__(self, config: dict):
        """ Add the database config parameters to the object.

        On Object creation, pass a dictionary with all relevant
        information on the connection to MySQL and store in attribute
        configuration.
        Minimum required key-value pairs:
        host -- ip address of host running MySQL
        user -- the MySQL username
        password -- of the user
        database -- name of database
        """
        self.configuration = config
        self.conn = None
        self.cursor = None

    def __enter__(self) -> 'cursor':
        """ Establish connection to mySQL.

        On established connection return a cursor object.
        Raise a ConnectionError if th database cannot be reached.
        Raise a CredentialsError if username and/or password are wrong.
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

        Raise an SQLError if the sql query code has errors.
        Raise a generic Error if an other error occurs.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type == mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        if exc_type:
            raise exc_type(exc_value)
