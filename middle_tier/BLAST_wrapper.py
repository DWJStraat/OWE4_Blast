import json

from Bio.Blast import NCBIWWW
from Bio import SeqIO
from colorama import Style
import xml.etree.ElementTree as ET
import winsound as ws


class BLAST_wrapper():
    """
    This class is a wrapper for the Bio.Blast library.
    """

    def __init__(self, sequence, database, name, debug=False, matrix='BLOSUM62'):
        self.hits = None
        self.xml = None
        self.result = None
        self.name = name
        self.sequence = sequence
        self.database = database
        self.debug = debug
        self.matrix = matrix

    def blast(self):
        """
        This function blasts the sequence against the database
        :return result_handle: the result of the blast
        """
        if not self.debug:
            print(f'{Style.DIM}BLASTing {self.name} against database {self.database}')
            self.result = NCBIWWW.qblast("blastn", self.database, self.sequence)
        else:
            print(f'{Style.DIM}BLASTing {self.name} against database {self.database}')
            self.result = open('test.xml', 'r')

        print(f'{Style.DIM} Finished BLASTing {self.name} against database {self.database}')
        print(f'{Style.RESET_ALL}')
        ws.Beep(1000, 100)

    def load_results(self):
        results = self.result.read()
        self.result.close()
        results = ET.fromstring(results)
        self.xml = results

    def get_first_x(self, x):
        """
        This function returns the first x results of the blast
        :param x: the number of results to return
        :return: the first x results
        """
        hits = "{}"
        hits = json.loads(hits)
        for child in self.xml.iter('Iteration'):
            run_id = child.find('Iteration_iter-num').text
            hits[run_id] = {}
            for hit in child.iter('Hit'):
                hit_num = hit.find('Hit_num').text
                if int(hit_num) > x:
                    break
                hits[run_id][hit_num] = {}
                for hit_child in hit:
                    hits[run_id][hit_num][hit_child.tag] = hit_child.text
                Hit_hsps = hit.find('Hit_hsps')
                hits[run_id][hit_num]['Hit_hsps'] = {}
                for hsp in Hit_hsps.iter('Hsp'):
                    hsp_num = hsp.find('Hsp_num').text
                    hits[run_id][hit_num]['Hit_hsps'][hsp_num] = {}
                    for hsp_child in hsp:
                        hits[run_id][hit_num]['Hit_hsps'][hsp_num][hsp_child.tag] = hsp_child.text

        self.hits = hits


if __name__ == '__main__':
    file = open('test.fasta', 'r').read()
    a = BLAST_wrapper(file, 'nt', name='test')
    a.blast()
    a.load_results()
    a.get_first_x(5)
