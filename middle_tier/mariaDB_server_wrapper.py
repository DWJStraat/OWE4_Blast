import mariadb


class server():
    """
    This class is a wrapper for the mariadb library.
    It is used to connect to a mariadb server and execute queries.
    """
    def __init__(self, host, user, password, database):
        """
        :param host: The host of the server
        :param user:
        :param password:
        :param database:
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """
        This function connects to the server and stores the connection in self.connection
        """
        try:
            self.connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return None

    def disconnect(self):
        """
        This function disconnects from the server
        """
        self.connection.close()

    def execute(self, query):
        """
        This function executes a query on the server
        :param query: the query to execute
        :return cursor: the result of the query
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor

    def commit(self):
        """
        This function commits the changes to the server
        """
        self.connection.commit()

    def getCursor(self):
        """
        This function creates a cursor for the server and stores it in self.cursor
        """
        self.cursor = self.connection.cursor()

    def closeCursor(self):
        """
        This function closes the cursor
        """
        self.cursor.close()
    def open(self):
        self.connect()
        self.getCursor()

    def close(self, commit=False):
        """
        This function closes the connection to the server
        :param commit: whether to commit the changes
        """
        if commit:
            self.commit()
        self.closeCursor()
        self.disconnect()

    def query(self, query, commit=False):
        """
        This function executes a query on the server and returns the result
        :param query: the query to execute
        :param commit: whether to commit the changes
        :return value: the result of the query
        """
        self.open()
        try:
            self.cursor.execute(query)
            try:
                value = self.cursor.fetchall()
            except mariadb.ProgrammingError:
                value = None
            self.close(commit)
        except mariadb.Error as e:
            self.close()
            print(f"Error: {e}\nQuery: {query}")
            raise e
        return value
