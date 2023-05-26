import mariadb
import os.path


class Server:
    """
    This class is a wrapper for the mariadb library.
    It is used to connect to a mariadb server and execute queries.
    """

    def __init__(self, host, user, password, database, port=3306):
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
        self.port = port

    def connect(self):
        """
        This function connects to the server and stores the connection in self.connection
        """
        try:
            self.connection = mariadb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return True
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return False

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

    def mass_insert(self, list_of_values, table, columns):
        """
        This function inserts a list of values into a table
        :param list_of_values: the values to insert
        :param table: the table to insert into
        :param columns: the columns to insert into
        """
        id = self.query(f"SELECT MAX(id) FROM {table};")[0][0]
        new_list = []
        if id is None:
            id = -1
        for value in list_of_values:
            id += 1
            value = (id,) + value
            new_list.append(value)
        columns = ", ".join(columns)
        query = f"INSERT INTO {table}({columns}) VALUES "
        for value in new_list:
            query += f"{value}, "
        query = f"{query[:-2]};"
        self.query(query, commit=True)

    def get_ID(self, table, collumn=None, value=None):
        """
        This function gets the next ID for a table
        :param value:
        :param collumn:
        :param table:
        :return:
        """
        if collumn is not None and value is not None:
            print(type(value))
            query = f"SELECT MAX(id) FROM {table} WHERE {collumn} = '{value}';"
            value = self.query(query)[0][0]
            if value is []:
                pass
            else:
                return value
        table_id = self.query(f"SELECT MAX(id) FROM {table};")[0][0]
        if table_id is None:
            table_id = -1
        return int(table_id + 1)

    def search(self, columns_to_select, parameters):
        """
        This function searches the database for a specific value
        :param columns_to_select: The columns to select
        :param parameters: The parameters to search for
        :return value: The resulting values
        """
        # Generates a table with all the information needed to display the results, which can be used to search through
        with open(os.path.split(os.path.dirname(__file__))[0] + r"\database\search.sql", "r") as f:
            table = f.read()
        query = f"SELECT {columns_to_select} FROM ({table}) as Br0 WHERE {parameters};"
        return self.query(query)

    # def enter_into_DB(self, json_data, enter_dna_seq = False, enter_responsible_machine=False, enter_process=False):
    #     """
    #     This function enters the data into the database
    #     """
    #     for entry_id in json_data:
    #         for hit in entry_id:
    #             for hsp in entry_id:
    #                 hit_def = hit["hit_def"].split(" ")
    #                 name = hit_def[1]
    #                 genus = hit_def[0]
    #                 accession = hit["acc"]
    #                 e_value = hsp["e_val"]
    #                 hit_len = hit["hit_len"]
    #                 score = hsp["score"]
    #                 query_end = hsp["query_end"]
    #                 query_star = hsp["query_start"]
    #                 bit_score = hsp["bit_score"]


if __name__ == '__main__':
    test = Server("145.74.104.144", "100006", "DeleteSys32", "A100006")
    print(test.search('test', 'test'))
