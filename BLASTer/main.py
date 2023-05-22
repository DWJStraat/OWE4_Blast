"""
The main file for the BLASTer program.
Created on 17-may-2023 by David
Collaborators: David
Last modified on 17-may-2023 by David
"""
from BLASTer import BLASTer as BLASTer
from reader import reader as reader


def main():
    """
    Main function for the BLASTer program.
    :return: None
    """
    # This part is for BLASTing all sequences in the database that haven't been blasted yet.
    BLAST = BLASTer()
    do_blast_input = input("Do you want to start a BLAST? (y/n): ")
    if do_blast_input == "y":
        BLAST.run()
    else:
        print("No BLAST started.")
    # This part is for reading the output of the BLASTs.
    read = reader()
    do_read_input = input("Do you want to start a read? (y/n): ")
    if do_read_input == "y":
        read.run()
        print('Finished reading.')

    else:
        print("No read started.")
    print("Program finished.")


main()
