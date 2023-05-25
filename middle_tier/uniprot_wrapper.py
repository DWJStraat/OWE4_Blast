"""
This file contains the Uniprot class which is a wrapper for the Uniprot API
It is currently not used in the project, yet kept for future use
Created on 22-may-2023 by David
Collaborators: David
Last modified on 25-may-2023 by David
"""
import requests


class Uniprot:
    """
    This class is a wrapper for the Uniprot API.
    """

    def __init__(self, acc_code):
        self.acc_code = acc_code
        self.url = f'https://www.uniprot.org/uniprot/{self.acc_code}.xml'
        self.xml = None

    def get_xml(self):
        """
        This function gets the xml of the protein from the Uniprot API and stores it in self.xml
        """
        self.xml = requests.get(self.url).text

    def get_prot_name(self):
        """
        This function returns the name of the protein
        :return: The full name of the protein given
        """
        if self.xml is None:
            self.get_xml()
        return self.xml.split('<fullName>')[1].split('</fullName>')[0]

    def get_lineage(self):
        """
        This function returns the lineage of the protein
        :return: A list of the lineage of the protein
        """
        if self.xml is None:
            self.get_xml()
        lineage = self.xml.split('<lineage>')[1].split('</lineage>')[0]
        lineage_list = []
        lineage = lineage.replace('<taxon>', '')
        lineage = lineage.replace('</taxon>', '\n')
        # Cycles through the lineage data and adds the contents to a list
        for line in lineage.split('\n'):
            line = line.strip()
            if line != '':
                lineage_list.append(line)
        # Adds the species to the list
        species = self.get_species().capitalize()
        lineage_list.append(species)
        return lineage_list

    def get_species(self):
        """
        This function returns the genus of the protein
        :return:
        """
        if self.xml is None:
            self.get_xml()
        organism = self.xml.split('<organism>')[1].split('</organism>')[0]
        scientific_name = organism.split('<name type="scientific">')[1].split('</name>')[0]
        return scientific_name.split(' ')[1]

