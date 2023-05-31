"""
This module fills the database with the data from the given data
Created on 17-may-2023 by David
Collaborators: David
Last modified on 31-may-2023 by David
"""

import json

from middle_tier.mariaDB_server_wrapper import Server as Server
from middle_tier.entrez_wrapper import EntrezWrapper as Entrez


class Filler(Entrez):
    """
    This class fills the database with the data from the given data
    """

    def __init__(self, server=None, acc_code=None, host=None, user=None, password=None, database=None, process_id=None,
                 port=3306):
        super().__init__(acc_code)
        self.seq_id = None
        self.process_id = process_id
        self.BLAST_result_id = None
        if server is None:
            self.server = Server(host, user, password, database, port)
            self.server.connect()
        else:
            self.server = server
        self.organism_id = self.server.get_ID('Organism')
        self.genus_id = self.server.get_ID('genus')
        self.prot_id = self.server.get_ID('Protein')
        self.prot_name_id = self.server.get_ID('Prot_name')
        self.name = self.get_prot_name()
        self.species = self.get_species()
        self.genus = self.get_genus()

    def prot_name(self):
        """
        This method inserts the protein name into the database
        """
        query = f"IF (SELECT COUNT(*) FROM Prot_name WHERE Name = '{self.name}') " \
                f"= 0 THEN INSERT INTO Prot_name (Name) VALUES ('{self.name}');" \
                f"END IF; " \
                f"SELECT ID FROM Prot_name WHERE Name = '{self.name}';"
        self.prot_name_id = self.server.query(query, commit=True)

    def protein(self):
        """
        This method inserts the protein into the database
        """
        query = f"IF (SELECT COUNT(*) FROM Protein WHERE prot_name_id = {self.prot_name_id}) " \
                f"= 0 THEN INSERT INTO Protein (prot_name_id) VALUES ({self.prot_name_id});" \
                f"END IF;" \
                f"SELECT ID FROM Protein WHERE prot_name_id = {self.prot_name_id};"
        self.prot_id = self.server.query(query, commit=True)

    def fill_genus(self):
        """
        This method inserts the genus into the database
        """
        query = f"IF (SELECT COUNT(*) FROM genus WHERE Name = '{self.genus}') " \
                f"= 0 THEN INSERT INTO Prot_name (Name) VALUES ('{self.genus}');" \
                f"END IF;" \
                f"SELECT ID FROM genus WHERE Name = '{self.genus}';"
        self.server.query(query, commit=True)

    def fill_species(self):
        """
        This method inserts the species into the database
        """
        if self.genus_id is None:
            self.fill_genus()
        if self.species is None:
            self.species = 'Unknown'
        query = f"IF (SELECT COUNT(*) FROM Organism WHERE Name = '{self.species}' AND genus_ID = {self.genus_id} ) " \
                f"= 0 THEN INSERT INTO Organism (Name, genus_ID) VALUES ('{self.species}', {self.genus_id});" \
                f"END IF;" \
                f"SELECT ID FROM Organism WHERE Name = '{self.species}' AND genus_ID = {self.genus_id};"
        self.server.query(query, commit=True)

    def BLAST_result(self, e_val, id_perc, query_cover, acc_len, max_score, total_score):
        """
        This method inserts the BLAST result into the database
        :param e_val: e value
        :param id_perc: identity percentage
        :param query_cover: query cover
        :param acc_len: accession length
        :param max_score: max score
        :param total_score: total score
        """
        if self.organism_id is None:
            self.organism_id = 'NULL'
        if self.prot_id is None:
            self.prot_id = 'NULL'
        query = f"INSERT INTO BLAST_result (E_val, Identity_percentage, Query_cover, Acc_len, Max_score, " \
                f"Total_score, Accession_code, DNA_seq_ID, Protein_ID, Organism_ID) VALUES  ({e_val}," \
                f"{id_perc}," \
                f"{query_cover}," \
                f"{acc_len}," \
                f"{max_score}," \
                f"{total_score}," \
                f"'{self.acc_code}'," \
                f"{self.seq_id}," \
                f"{self.prot_id}," \
                f"{self.organism_id})"
        print(query)
        self.server.query(query, commit=True)

    def get_seq_id(self):
        """
        This method gets the sequence id from the database
        """
        query = f'SELECT DNA_seq_id FROM Process WHERE ID = {self.process_id}'
        print(query)
        result = self.server.query(query)
        try:
            self.seq_id = result[0][0]
        except IndexError:
            self.seq_id = None

    def fill(self, e_val, id_perc, query_cover, acc_len, max_score, total_score):
        """
        This method fills the database with the data from the given data
        :param e_val:
        :param id_perc:
        :param query_cover:
        :param acc_len:
        :param max_score:
        :param total_score:
        """
        self.get_seq_id()
        self.fill_genus()
        self.fill_species()
        self.prot_name()
        self.protein()
        self.BLAST_result(e_val, id_perc, query_cover, acc_len, max_score, total_score)


class MassFiller:
    """
    This class is used to fill the database with data from a json file
    """

    def __init__(self, json_file, config_file):
        # sourcery skip: raise-specific-error
        self.filler = None
        self.json_file = json_file
        self.config = json.load(config_file)
        host = self.config['host']
        user = self.config['user']
        password = self.config['password']
        database = self.config['database']
        self.server = Server(host, user, password, database)
        self.data = None
        if self.server.connect():
            print('Connected to the database')
        else:
            print('Could not connect to the database')
            raise Exception('Could not connect to the database')

    def read_json(self):
        """
        This method reads the json file
        """
        with open(self.json_file) as json_file:
            data = json.load(json_file)
        self.data = data

    def process(self):
        """
        This method processes the data from the json file
        """
        for entry in self.data:
            print(f'Filling entry {entry}')
            data = self.data[entry]
            # update_process_pre_entry = f'UPDATE Process SET Status = 2 WHERE ID = {entry}'
            # self.server.query(update_process_pre_entry, commit=True)
            if data is not None:
                process_id = entry
                for protein in data:
                    for hsp in data[protein]:
                        print('Data is not None')
                        hsp = data[protein][hsp]
                        print(hsp)
                        acc_code = hsp['acc']
                        e_val = str(hsp['e_val'])
                        id_perc = hsp['identity']
                        query_cover = hsp['query_cover']
                        acc_len = hsp['hit_len']
                        max_score = hsp['score']
                        total_score = hsp['bit_score']
                        print('Creating filler')
                        self.filler = Filler(self.server, acc_code=acc_code, process_id=int(process_id))
                        print('Filling')
                        print(e_val)
                        self.filler.fill(e_val, id_perc, query_cover, acc_len, max_score, total_score)
            update_process = f'UPDATE Process SET Status = 3 WHERE ID = {entry}'
            self.server.query(update_process, commit=True)

    def run(self):
        """
        This method runs the class
        """
        self.read_json()
        self.process()


if __name__ == "__main__":
    jsonfile = 'results1685002823.json'
    config = open('config.json')
    filler = MassFiller(jsonfile, config)
