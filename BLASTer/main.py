"""
The main file for the BLASTer program.
Created on 17-may-2023 by David
Collaborators: David
Last modified on 17-may-2023 by David
"""

from BLASTer import BLASTer as BLASTer
from filler import MassFiller
from reader import Reader


def main():
    """
    Main function for the BLASTer program.
    :return: None
    """
    # This part is for BLASTing all sequences in the database that haven't
    # been blasted yet.
    BLAST = BLASTer()
    do_blast_input = input("Do you want to start a BLAST? (y/n): ")
    if do_blast_input == "y":
        BLAST.run()
    else:
        print("No BLAST started.")
    # This part is for reading the output of the BLASTs.
    do_read_input = input("Do you want to start a read? (y/n): ")
    if do_read_input == "y":
        read = Reader()
        print('Finished reading.')
        do_export = input(
            "Do you want to export the results to a JSON file? (y/n): ")
        if do_export == "y":
            do_delete = input("Do you want to delete the XML files? (y/n): ")
            if do_delete == "y":
                read.export()
            else:
                read.export(False)
    else:
        print("No read started.")
    do_import = input(
        "Do you want to import the results from a JSON file? (y/n): ")
    if do_import == "y":
        file_name = input(
            "Please enter the name of the file you want to import: ")
        try:
            results = file_name
        except FileNotFoundError:
            print("File not found.")
            return
    else:
        print("No import started.")
        results = None
    if results is not None:
        do_enter = input(
            "Do you want to enter the results into the database? (y/n): ")
        if do_enter == "y":
            filler = MassFiller(results, open("config.json", "r"))
            filler.run()
            print("Finished entering.")
        else:
            print("No entering started.")
    print("Program finished.")


main()
