"""
This module BLASTs all sequences in the database that
haven't been blasted yet.
Created on 17-may-2023 by David
Collaborators: David
Last modified on 17-may-2023 by David
"""

import json
import sys

sys.path.insert(0, "../")

from middle_tier import mariaDB_server_wrapper as MariaDB
from middle_tier import BLAST_wrapper as Blast
import random
import socket


class BLASTer:
    """
    This class is the main class for the BLASTer program.
    """

    def __init__(self, debug=False):
        self.seq = None
        self.header = None
        self.blast = None
        self.quality = None
        self.process_id = None
        self.ip = None
        self.hostname = None
        self.machine_id = None
        self.id = None
        self.debug = debug
        self.blast_results = json.loads("{}")
        self.config = json.load(open("config.json", "r"))
        self.server = MariaDB.Server(
            self.config["host"],
            self.config["user"],
            self.config["password"],
            self.config["database"]
        )
        self.find_next()
        self.get_my_id()

    def find_next(self):
        """
        Finds the next sequence that needs to be BLASTed.
        :return: True if a sequence was found, False if not.
        """
        query = "SELECT ID FROM DNA_seq WHERE ID not in " \
                "(SELECT DNA_seq_ID FROM Process);"
        available_sequences = self.server.query(query)
        if len(available_sequences) == 0:
            return False
        self.id = random.choice(available_sequences)[0]
        return True

    def get_my_id(self):
        """
        Gets the ID of the machine running this program, and inserts
        it if it's not present in the database.
        """
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        this_machine_id = self.server.query(f"SELECT ID FROM "
                                            f"Responsible_Machine "
                                            f"WHERE IP = '{self.ip}';")
        if len(this_machine_id) == 0:
            this_machine_id = self.server.get_ID('Responsible_Machine')
            self.server.query(f"INSERT INTO Responsible_Machine "
                              f"(ID, IP, Name) "
                              f"VALUES ('{this_machine_id}', '{self.ip}', '"
                              f"{self.hostname}');", True)
            print(f"New machine added with ID: {this_machine_id}")
        else:
            this_machine_id = this_machine_id[0][0]
            print(f"Machine found with ID: {this_machine_id}")
        self.machine_id = this_machine_id

    def start_blast(self):
        """
        Starts the BLAST process.
        """
        self.process_id = self.server.get_ID('Process')
        query = f'INSERT INTO Process (ID, Status, DNA_seq_ID, ' \
                f'Responsible_Machine_ID) ' \
                f'VALUES ({self.process_id},0, {self.id}, {self.machine_id});'
        if not self.debug:
            self.server.query(query, True)
            seq_data = self.server.query(f'SELECT * FROM DNA_seq WHERE ID = '
                                         f'{self.id};')[0]
        else:
            seq_data = ['1', 'header', 'quality', 'ATCG']
        self.quality = seq_data[2]
        self.seq = seq_data[3]
        self.header = seq_data[1]
        print(self.seq)
        self.blast = Blast.BLASTwrapper(self.seq, 'nt', self.header,
                                        program='blastx',
                                        debug=self.debug,
                                        process=self.process_id, expect=0.05)
        self.blast.blast()
        # self.blast.load_results()
        self.blast.get_first_x(15)
        if not self.debug:
            self.server.query(f'UPDATE Process SET Status = 1 '
                              f'WHERE ID = {self.process_id};', True)

    def run(self):
        """
        Runs the BLASTer program.
        """
        while self.find_next():
            self.start_blast()
        print("No more sequences to BLAST.")
