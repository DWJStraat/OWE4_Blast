import openpyxl
import json
class excel():
    def __init__(self, excel):
        self.db_data = None
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

    def parse_for_db(self, use_json=True):
        data = json.loads('{}')
        values = []
        id = 0
        for row in self.sheet.iter_rows():
            if use_json:
                data[id] = json.loads('{}')
                data[id]["header"] = row[0].value
                data[id]["sequence"] = row[1].value
                data[id]["quality"] = row[2].value
                id += 1
                data[id] = json.loads('{}')
                data[id]["header"] = row[3].value
                data[id]["sequence"] = row[4].value
                data[id]["quality"] = row[5].value
                id += 1
            else:
                values += (row[0].value, row[1].value, row[2].value), (row[3].value, row[4].value, row[5].value)
        self.db_data = data
        self.values = values


if __name__ == "__main__":
    a = excel("Map1.xlsx")
    a.parse_for_db(use_json=False)