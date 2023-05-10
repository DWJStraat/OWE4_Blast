import openpyxl
import json
class excel():
    def __init__(self, excel):
        if type(excel) is str:
            self.excel = open(excel, "r")
            self.excel_name = excel
        else:
            self.excel = excel
            self.excel_name = excel.name
        self.df = openpyxl.load_workbook(self.excel_name)
        self.sheet = self.df.active
        self.entries = []
        self.parse()

    def parse(self):
        for row in self.sheet.iter_rows():
            val = json.loads('{}')
            val["fwd_header"] = row[0].value
            val["fwd_seq"] = row[1].value
            val["fwd_qual"] = row[2].value
            val["rev_header"] = row[3].value
            val["rev_seq"] = row[4].value
            val["rev_qual"] = row[5].value
            self.entries.append(val)

a = excel("Map1.xlsx")
