import json

from middle_tier import mariaDB_server_wrapper as MariaDB
from middle_tier import BLAST_wrapper as BLAST
import random
import socket


class BLASTer():
    def __init__(self):
        self.machine_id = None
        self.id = None
        self.config = json.load(open("config.json", "r"))
        self.server = MariaDB.server(
            self.config["host"],
            self.config["user"],
            self.config["password"],
            self.config["database"]
        )

    def find_next(self):
        query = "SELECT ID FROM DNA_seq WHERE ID not in (SELECT DNA_seq_ID FROM Process);"
        available_sequences = self.server.query(query)
        if len(available_sequences) == 0:
            return None
        else:
            self.id = random.choice(available_sequences)[0]

    def get_my_id(self):
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        machine_id = self.server.query(f"SELECT ID FROM Responsible_Machine WHERE IP = '{self.ip}';")
        if len(machine_id) == 0:
            machine_id = self.server.get_ID('Responsible_Machine')
            self.server.query(f"INSERT INTO Responsible_Machine (ID, IP, Name) "
                              f"VALUES ('{machine_id}', '{self.ip}', '{self.hostname}');", True)
            print(f"New machine added with ID: {machine_id}")
        self.machine_id = machine_id

    def start_blast(self):
        self.process_id = self.server.get_ID('Process')
        query = f'INSERT INTO Process (ID, Status, DNA_seq_ID, Responsible_Machine_ID) ' \
                f'VALUES ({self.process_id},0, {self.id}, {self.machine_id});'
        self.server.query(query, True)
        seq_data = self.server.query(f'SELECT * FROM DNA_seq WHERE ID = {self.id};')[0]
        self.quality = seq_data[2]
        self.seq = seq_data[1]
        self.header = seq_data[0]
        self.blast = BLAST.BLAST_wrapper(self.seq, 'nt', self.header)
        self.blast.blast()
        self.blast.get_first_x(15)
        self.server.query(f'UPDATE Process SET Status = 1 WHERE ID = {self.process_id};', True)


def main():
    blast = BLASTer()
    blast.get_my_id()
    blast.find_next()
    blast.start_blast()
    print("No more sequences to BLAST")
    return blast

blast = main()