"""
This module is a wrapper for the Entrez module of BioPython and
interfaces with the NCBI database
Created on 22-may-2023 by David
Collaborators: David
Last modified on 22-may-2023 by David
"""
import json
import time
from pathlib import Path

import Bio.Entrez as Entrez


class EntrezWrapper:
    """
    This class is a wrapper for the Entrez module of BioPython and
    interfaces with the NCBI database
    """

    def __init__(self, acc_code, sleep_between_tries=10, max_tries=10,
                 db='protein'):
        self.record = None
        config = json.load(open(Path('../config.json')))
        self.email = config['email']
        self.acc_code = acc_code
        self.sleep_between_tries = sleep_between_tries
        self.max_tries = max_tries
        self.db = db

    def get_entrez(self):
        """
        This method fetches the record from the NCBI database
        """
        time.sleep(3)
        print(f'Fetching {self.acc_code}')
        handle = Entrez.efetch(db=self.db,
                               id=self.acc_code,
                               retmode='xml',
                               email=self.email,
                               sleep_between_tries=self.sleep_between_tries,
                               max_tries=self.max_tries)
        self.record = Entrez.read(handle)
        print(f'Fetched {self.acc_code}')
        handle.close()

    def get_prot_name(self):
        """
        This method returns the name of the protein
        :return: str - name of the protein
        """
        if self.record is None:
            self.get_entrez()
        return self.record[0]['GBSeq_definition']

    def get_lineage(self):
        """
        This method returns the lineage of the organism associated
        :return: list - lineage of the organism associated
        """
        if self.record is None:
            self.get_entrez()
        return self.record[0]['GBSeq_taxonomy'].split('; ')

    def get_full(self):
        """
        This method returns the full record of the protein
        :return: ListElement - full record of the protein
        """
        if self.record is None:
            self.get_entrez()
        return self.record

    def get_organism(self):
        """
        This method returns the organism associated with the protein
        :return: str - organism associated with the protein
        """
        if self.record is None:
            self.get_entrez()
        return self.record[0]['GBSeq_organism']

    def get_genus(self):
        """
        This method returns the genus of the organism associated with
        the protein
        :return: str - genus of the organism associated with the protein
        """
        return self.get_lineage()[-1]

    def get_species(self):
        """
        This method returns the species of the organism associated with
        the protein
        :return: str - species of the organism associated with the protein
        """
        print(self.get_organism())
        try:
            return self.get_organism().split(' ')[1].capitalize()
        except IndexError:
            return self.get_organism().capitalize()