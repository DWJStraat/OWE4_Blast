import json

from middle_tier.mariaDB_server_wrapper import Server as Server
from middle_tier.entrez_wrapper import EntrezWrapper as Entrez


class Filler(Entrez):
    """
    This class fills the database with the data from the given data
    """

    def __init__(self, acc_code, host, user, password, database, process_id, port=3306):
        super().__init__(acc_code)
        self.seq_id = None
        self.process_id = process_id
        self.BLAST_result_id = None
        self.organism_id = None
        self.genus_id = None
        self.prot_id = None
        self.prot_name_id = None
        self.name = self.get_prot_name()
        self.species = self.get_species()
        self.genus = self.get_genus()
        self.server = Server(host, user, password, database, port)

    def prot_name(self):
        """
        This method inserts the protein name into the database
        """
        name = self.name
        self.prot_name_id = int(self.server.get_ID('Prot_name', 'Name', name))
        query = f"IF (SELECT COUNT(*) FROM Prot_name WHERE Name = '{name}') " \
                f"= 0 THEN INSERT INTO Prot_name VALUES ({self.prot_name_id}, '{name}');" \
                f"END IF;"
        print(query)
        self.server.query(query, commit=True)

    def protein(self):
        """
        This method inserts the protein into the database
        """
        self.prot_id = int(self.server.get_ID('Protein', 'prot_name_id', self.prot_name_id))
        query = f"IF (SELECT COUNT(*) FROM Protein WHERE prot_name_id = {self.prot_name_id}) " \
                f"= 0 THEN INSERT INTO Protein VALUES ({self.prot_id}, {self.prot_name_id});" \
                f"END IF;"
        self.server.query(query, commit=True)

    def fill_genus(self):
        """
        This method inserts the genus into the database
        """
        self.genus_id = int(self.server.get_ID('genus', 'Name', self.genus))
        query = f"IF (SELECT COUNT(*) FROM genus WHERE Name = '{self.genus}') " \
                f"= 0 THEN INSERT INTO Prot_name VALUES ({self.genus_id}, '{self.genus}');" \
                f"END IF;"
        self.server.query(query, commit=True)

    def fill_species(self):
        """
        This method inserts the species into the database
        """
        self.organism_id = int(self.server.get_ID('Organism', 'Name', self.species))
        if self.genus_id is None:
            self.fill_genus()
        if self.species is None:
            self.species = 'Unknown'
        query = f"IF (SELECT COUNT(*) FROM Organism WHERE Name = '{self.species}' AND genus_ID = {self.genus_id} ) " \
                f"= 0 THEN INSERT INTO Organism VALUES ({self.organism_id}, '{self.species}', {self.genus_id});" \
                f"END IF;"
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
        self.BLAST_result_id = int(self.server.get_ID('BLAST_result'))
        if self.organism_id is None:
            self.organism_id = 'NULL'
        if self.prot_id is None:
            self.prot_id = 'NULL'
        query = f"INSERT INTO BLAST_result VALUES ({self.BLAST_result_id}, " \
                f"{e_val}," \
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
        self.seq_id = int(self.server.query(query)[0][0])

    def fill_organism(self):
        self.fill_genus()
        self.fill_species()

    def fill_protein(self):
        self.prot_name()
        self.protein()

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
        self.fill_organism()
        self.fill_protein()
        self.BLAST_result(e_val, id_perc, query_cover, acc_len, max_score, total_score)

class MassFiller():
    def __init__(self, json_file, config_file):
        self.json_file = json_file
        self.config = json.load(config_file)
        host = self.config['host']
        user = self.config['user']
        password = self.config['password']
        database = self.config['database']
        self.server = Server(host, user, password, database)

    def read_json(self):
        with open(self.json_file) as json_file:
            data = json.load(json_file)
        self.data = data

    def process(self):
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
                        e_val = hsp['e_val']
                        id_perc = hsp['identity']
                        query_cover = hsp['query_cover']
                        acc_len = hsp['hit_len']
                        max_score = hsp['score']
                        total_score = hsp['bit_score']
                        print('Creating filler')
                        filler = Filler(acc_code, self.config['host'], self.config['user'], self.config['password'],
                                        self.config['database'], process_id)
                        print('Filling')
                        filler.fill(e_val, id_perc, query_cover, acc_len, max_score, total_score)
            update_process = f'UPDATE Process SET Status = 3 WHERE ID = {entry}'
            self.server.query(update_process, commit=True)

    def run(self):
        self.read_json()
        self.process()
