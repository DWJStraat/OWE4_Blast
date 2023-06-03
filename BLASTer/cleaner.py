import os
import sys
import json

sys.path.insert(0, "../")
from middle_tier.mariaDB_server_wrapper import Server as Server

config = json.load(open("config.json", "r"))
xmls = [file for file in os.listdir() if file.endswith(".xml")]
errorstring = 'Error'
error_nos = []
server = Server(
    config["host"],
    config["user"],
    config["password"],
    config["database"]
)
Processes = server.query('SELECT ID FROM Process;')
for xml in xmls:
    try:
        with open(xml) as f:
            delete = errorstring in f.read()
        if delete:
            os.remove(xml)
            server.query(f'DELETE FROM Process WHERE ID = {xml[:-4]};',
                         commit=True)
            error_nos.append(xml[:-4])
    except Exception as e:
        print(e)


xml_nos = [int(xml[:-4]) for xml in xmls]
for process in Processes:
    if process[0] not in xml_nos:
        server.query(f'DELETE FROM Process WHERE ID = {process[0]};',
                     commit=True)
        error_nos.append(process[0])