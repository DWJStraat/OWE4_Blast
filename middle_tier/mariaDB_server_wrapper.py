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
        self.connection.close()

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor

    def commit(self):
        self.connection.commit()

    def getCursor(self):
        self.cursor = self.connection.cursor()

    def closeCursor(self):
        self.cursor.close()
    def open(self):
        self.connect()
        self.getCursor()

    def close(self, commit=False):
        if commit:
            self.commit()
        self.closeCursor()
        self.disconnect()

    def query(self, query, commit=False):
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
