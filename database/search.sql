# The query used in the MariaDB Wrapper to get the data from the database
SELECT DISTINCT(DNA_seq.ID),
               Br.E_val,
               Br.Identity_percentage,
               Br.Query_cover,
               Br.Acc_len,
               Br.Max_score,
               Br.Total_score,
               Br.Accession_code,
               Organism.Name  as org_name,
               genus.Name     as org_genus,
               Prot_name.Name as Prot_name,
               seq_header,
               sequence
FROM BLAST_result,
     Organism,
     genus,
     Protein,
     Prot_name,
     DNA_seq
         LEFT JOIN BLAST_result Br on DNA_seq.ID = Br.DNA_seq_ID
         LEFT JOIN Organism O on Br.Organism_ID = O.ID
         LEFT JOIN genus g on O.genus_ID = g.ID
         LEFT JOIN Protein P on Br.Protein_ID = P.ID
         LEFT JOIN Prot_name Pn on P.Prot_name_ID = Pn.ID