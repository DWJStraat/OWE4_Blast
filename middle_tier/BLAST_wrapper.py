

import json
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from colorama import Style
import xml.etree.ElementTree as ET
import winsound as ws
from time import time

class BLASTwrapper():
    """
    This class is a wrapper for the Bio.Blast library.
    """

    def __init__(self, sequence, database, name, debug=False, matrix='BLOSUM62', process = 0, program = 'blastx'):
        self.hits = None
        self.xml = None
        self.result = None
        self.name = name
        self.sequence = sequence
        self.database = database
        self.debug = debug
        self.matrix = matrix
        self.process = process
        self.program = program

    def blast(self):
        """
        This function blasts the sequence against the database
        :return result_handle: the result of the blast
        """
        if not self.debug:
            timestamp = time()
            print(f'{Style.DIM}BLASTing {self.name} against database {self.database} at {timestamp}')
            self.result = NCBIWWW.qblast(self.program, self.database, self.sequence, alignments=15, megablast=True)
        else:
            print(f'{Style.DIM}BLASTing {self.name} against database {self.database}')
            self.result = open('test.xml', 'r')

        print(f'{Style.DIM} Finished BLASTing {self.name} against database {self.database}')
        print(f'{Style.RESET_ALL}')
        ws.Beep(1000, 100)
        with open(f'{self.process}.xml', 'x') as f:
            f.write(self.result.read())

    def load_results(self):
        results = self.result.read()
        self.result.close()
        results = ET.fromstring(results)
        self.xml = results

    # def get_first_x(self, x):
    #     """
    #     This function returns the first x results of the blast
    #     :param x: the number of results to return
    #     :return: the first x results
    #     """
    #     self.load_results()
    #     hits = "{}"
    #     hits = json.loads(hits)
    #     for child in self.xml.iter('Iteration'):
    #         run_id = child.find('Iteration_iter-num').text
    #         hits[run_id] = {}
    #         for hit in child.iter('Hit'):
    #             hit_num = hit.find('Hit_num').text
    #             if int(hit_num) > x:
    #                 break
    #             hits[run_id][hit_num] = {}
    #             for hit_child in hit:
    #                 hits[run_id][hit_num][hit_child.tag] = hit_child.text
    #             Hit_hsps = hit.find('Hit_hsps')
    #             hits[run_id][hit_num]['Hit_hsps'] = {}
    #             for hsp in Hit_hsps.iter('Hsp'):
    #                 hsp_num = hsp.find('Hsp_num').text
    #                 hits[run_id][hit_num]['Hit_hsps'][hsp_num] = {}
    #                 for hsp_child in hsp:
    #                     hits[run_id][hit_num]['Hit_hsps'][hsp_num][hsp_child.tag] = hsp_child.text
    #
    #     self.hits = hits

    def get_first_x(self, x):
        self.hits = []
        records = NCBIXML.parse(open(f'{self.process}.xml', 'r'))
        records = next(records)
        self.records = records
        for alignment in records.alignments:
            self.hits.append(alignment)

    def export_xml(self):
        with open(f'{self.name}.xml', 'w') as f:
            f.write(self.result.read())
            f.close()

if __name__ == '__main__':
    file = open('test.fasta', 'r').read()
    a = BLASTwrapper(file, 'nt', name='test')
    a.blast()
    a.load_results()
    a.get_first_x(15)
    a.export_xml()