"""
This module reads the xml files and stores the results in a dictionary
Created on 22-may-2023 by David
Collaborators: David
Last modified on 22-may-2023 by David
"""

import os
from Bio.Blast import NCBIXML
import json
import time


class Reader:
    """
    This class reads the xml files and stores the results in a dictionary
    """

    def __init__(self):
        self.files = None
        self.results = None
        self.find_files()
        self.read_files()

    def find_files(self):
        """
        This function finds all the xml files in the current directory
        """
        files = [file for file in os.listdir() if file.endswith(".xml")]
        self.files = files

    def read_files(self):
        """
        This function reads the xml files and stores the results in a dictionary
        """
        self.results = json.loads("{}")
        for file in self.files:
            with open(file, "r") as f:
                file_id = file.split(".")[0]
                # Parse the xml file
                records = NCBIXML.parse(f)
                records2 = next(records)
                self.results[file_id] = {}
                # Iterate through the alignments and hsps and store the results in a JSON variable
                for alignment in records2.alignments:
                    self.results[file_id][alignment.hit_def] = {}
                    for hsp in alignment.hsps:
                        num = hsp.score
                        self.results[file_id][alignment.hit_def][num] = {
                            "hit_def": alignment.hit_def,
                            "acc": alignment.accession,
                            "e_val": hsp.expect,
                            "hit_len": alignment.length,
                            "score": hsp.score,
                            "bit_score": hsp.bits,
                            "query_start": hsp.query_start,
                            "query_end": hsp.query_end,
                            "hit_start": hsp.sbjct_start,
                            "hit_end": hsp.sbjct_end,
                            "query_cover": hsp.align_length / alignment.length,
                            "identity": hsp.identities / hsp.align_length,
                        }
                if len(self.results[file_id]) == 0:
                    self.results[file_id] = None

    def export(self, delete=True):
        """
        This function saves the results in a json file
        :param delete: Boolean, if True the xml files will be deleted. Default is True
        """
        with open(f"results{int(time.time())}", "x") as f:
            json.dump(self.results, f)
        if delete:
            for file in self.files:
                os.remove(file)


reader = Reader()
reader.find_files()
reader.read_files()
