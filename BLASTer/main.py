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
            machine_id = (
                    self.server.query("SELECT MAX(ID) FROM Responsible_Machine;")[0][0]
                    + 1
            )
            self.server.query(f"INSERT INTO Responsible_Machine (ID, IP, Name) VALUES ('{machine_id}', '{self.ip}', '{self.hostname}');")
        self.machine_id = machine_id




    def start_blast(self):
        self.process_id = self.server.query('SELECT MAX(ID) FROM Process')[0][0] + 1
        self.server.query(f'INSERT INTO Process (ID, Status, DNA_seq_ID, ) VALUES ({self.process_id}, {self.id});')
