-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-05-29 10:19:50.436

-- tables
-- Table: BLAST_result
CREATE TABLE BLAST_result (
    ID int NOT NULL AUTO_INCREMENT,
    E_val varchar(32) NULL,
    Identity_percentage decimal(5,2) NULL,
    Query_cover varchar(32) NULL,
    Acc_len int NULL,
    Max_score int NULL,
    Total_score int NULL,
    Accession_code varchar(30) NULL,
    DNA_seq_ID int NOT NULL,
    Protein_ID int NOT NULL,
    Organism_ID int NOT NULL,
    CONSTRAINT BLAST_result_pk PRIMARY KEY (ID)
);

-- Table: DNA_seq
CREATE TABLE DNA_seq (
    ID int NOT NULL AUTO_INCREMENT,
    seq_header char(120) NOT NULL,
    quality varchar(10000) NOT NULL,
    sequence varchar(10000) NOT NULL,
    CONSTRAINT DNA_seq_pk PRIMARY KEY (ID)
);

-- Table: Organism
CREATE TABLE Organism (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(256) NOT NULL,
    genus_ID int NOT NULL,
    CONSTRAINT Organism_pk PRIMARY KEY (ID)
);

-- Table: Process
CREATE TABLE Process (
    ID int NOT NULL AUTO_INCREMENT,
    Status int NOT NULL,
    DNA_seq_ID int NOT NULL,
    Responsible_Machine_ID int NOT NULL,
    CONSTRAINT Process_pk PRIMARY KEY (ID)
);

-- Table: Prot_name
CREATE TABLE Prot_name (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(256) NOT NULL,
    CONSTRAINT Prot_name_pk PRIMARY KEY (ID)
);

-- Table: Protein
CREATE TABLE Protein (
    ID int NOT NULL AUTO_INCREMENT,
    Prot_name_ID int NOT NULL,
    CONSTRAINT Protein_pk PRIMARY KEY (ID)
);

-- Table: Responsible_Machine
CREATE TABLE Responsible_Machine (
    ID int NOT NULL AUTO_INCREMENT,
    IP varchar(20) NOT NULL,
    Name varchar(256) NULL,
    CONSTRAINT Responsible_Machine_pk PRIMARY KEY (ID)
);

-- Table: genus
CREATE TABLE genus (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(32) NOT NULL,
    CONSTRAINT genus_pk PRIMARY KEY (ID)
);

-- Table: status_def
CREATE TABLE status_def (
    ID int NOT NULL AUTO_INCREMENT,
    state varchar(12) NOT NULL,
    Process_ID int NOT NULL,
    CONSTRAINT status_def_pk PRIMARY KEY (ID)
);

-- foreign keys
-- Reference: BLAST_result_DNA_seq (table: BLAST_result)
ALTER TABLE BLAST_result ADD CONSTRAINT BLAST_result_DNA_seq FOREIGN KEY BLAST_result_DNA_seq (DNA_seq_ID)
    REFERENCES DNA_seq (ID);

-- Reference: Organism_BLAST_result (table: BLAST_result)
ALTER TABLE BLAST_result ADD CONSTRAINT Organism_BLAST_result FOREIGN KEY Organism_BLAST_result (Organism_ID)
    REFERENCES Organism (ID);

-- Reference: Organism_Org_name (table: Organism)
ALTER TABLE Organism ADD CONSTRAINT Organism_Org_name FOREIGN KEY Organism_Org_name (genus_ID)
    REFERENCES genus (ID);

-- Reference: Process_DNA_seq (table: Process)
ALTER TABLE Process ADD CONSTRAINT Process_DNA_seq FOREIGN KEY Process_DNA_seq (DNA_seq_ID)
    REFERENCES DNA_seq (ID);

-- Reference: Protein_BLAST_result (table: BLAST_result)
ALTER TABLE BLAST_result ADD CONSTRAINT Protein_BLAST_result FOREIGN KEY Protein_BLAST_result (Protein_ID)
    REFERENCES Protein (ID);

-- Reference: Protein_Prot_name (table: Protein)
ALTER TABLE Protein ADD CONSTRAINT Protein_Prot_name FOREIGN KEY Protein_Prot_name (Prot_name_ID)
    REFERENCES Prot_name (ID);

-- Reference: Responsible_Machine_Process (table: Process)
ALTER TABLE Process ADD CONSTRAINT Responsible_Machine_Process FOREIGN KEY Responsible_Machine_Process (Responsible_Machine_ID)
    REFERENCES Responsible_Machine (ID);

-- Reference: status_def_Process (table: status_def)
ALTER TABLE status_def ADD CONSTRAINT status_def_Process FOREIGN KEY status_def_Process (Process_ID)
    REFERENCES Process (ID);

-- End of file.

