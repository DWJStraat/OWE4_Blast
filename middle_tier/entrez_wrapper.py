"""
This module is a wrapper for the Entrez module of BioPython and interfaces with the NCBI database
Created on 22-may-2023 by David
Collaborators: David
Last modified on 22-may-2023 by David
"""
import Bio.Entrez as Entrez
import json
from pathlib import Path


class EntrezWrapper:
    """
    This class is a wrapper for the Entrez module of BioPython and interfaces with the NCBI database
    """

    def __init__(self, acc_code):
        config = json.load(open(Path('../config.json')))
        self.email = config['email']
        self.acc_code = acc_code

    def get_prot_name(self):
        """
        This method returns the name of the protein
        :return: str - name of the protein
        """
        handle = Entrez.efetch(db='protein', id=self.acc_code, retmode='xml', email=self.email)
        record = Entrez.read(handle)
        handle.close()
        return record[0]['GBSeq_definition']

    def get_lineage(self):
        """
        This method returns the lineage of the organism associated
        :return: list - lineage of the organism associated
        """
        handle = Entrez.efetch(db='protein', id=self.acc_code, retmode='xml', email=self.email)
        record = Entrez.read(handle)
        handle.close()
        return record[0]['GBSeq_taxonomy'].split('; ')

    def get_full(self):
        """
        This method returns the full record of the protein
        :return: ListElement - full record of the protein
        """
        handle = Entrez.efetch(db='protein', id=self.acc_code, retmode='xml', email=self.email)
        record = Entrez.read(handle)
        handle.close()
        return record

    def get_organism(self):
        """
        This method returns the organism associated with the protein
        :return: str - organism associated with the protein
        """
        handle = Entrez.efetch(db='protein', id=self.acc_code, retmode='xml', email=self.email)
        record = Entrez.read(handle)
        handle.close()
        return record[0]['GBSeq_organism']

    def get_genus(self):
        """
        This method returns the genus of the organism associated with the protein
        :return: str - genus of the organism associated with the protein
        """
        return self.get_lineage()[-1]
    def get_species(self):
        """
        This method returns the species of the organism associated with the protein
        :return: str - species of the organism associated with the protein
        """
        return self.get_organism().split(' ')[1].capitalize()




a = EntrezWrapper('NP_001191.1')
