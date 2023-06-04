# The query used in the MariaDB Wrapper to get the data from the database
SELECT DNA_seq.ID,
       Br.E_val,
       Br.Identity_percentage,
       Br.Query_cover,
       Br.Acc_len,
       Br.Max_score,
       Br.Total_score,
       Br.Accession_code,
       CONCAT(G.Name, ' ', O.Name) as organism,
       Pn.Name as Prot_name,
       DNA_seq.seq_header,
       DNA_seq.sequence
from DNA_seq
         INNER JOIN BLAST_result Br on DNA_seq.ID = Br.DNA_seq_ID
         INNER JOIN Organism O on O.ID = Br.Organism_ID
         INNER JOIN genus G on G.ID = O.genus_ID
         INNER JOIN Process Pc on DNA_seq.ID = Pc.DNA_seq_ID
         INNER JOIN Protein Pt on Br.Protein_ID = Pt.ID
         INNER JOIN Prot_name Pn on Pt.Prot_name_ID = Pn.ID
