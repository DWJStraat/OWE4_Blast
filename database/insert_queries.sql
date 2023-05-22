insert into Prot_name values ({id}, {name});

insert into Protein values ({id}, {prot_name_id}(select ID from Prot_name));

insert into genus values ({id}, {name});

insert into Organism values ({id}, {name}, {genus_id}(select ID from genus));

insert into DNA_seq values ({id}, {accession_code}, {quality}, {sequence});

insert into BLAST_result values ({E_val},
                             {identity_percentage},
                             {query_cover},
                             {acc_len}, {max_score},
                             {total_score},
                             {accession_code},
                             {ID_placeholders},
                             {DNA_seq_id}(select ds.ID from DNA_seq ds left join BLAST_result br on ds.ID = br.ID limit 1),
                             {protein_id}(select p.ID from Protein p left join BLAST_result br on p.ID = br.ID limit 1),
                             {organism_id}(select o.ID from Organism o left join BLAST_result br on o.ID = br.ID limit 1));

insert into Responsible_Machine values ({id}, {ip}, {name});

insert into Process values (1, 2,
                            {dna_seq_id}(select ds.ID from DNA_seq ds
                                left join Process p on ds.ID = p.ID limit 1),
                            {responsible_machine_id}(select ds.ID from DNA_seq ds
                                left join Responsible_Machine rm on ds.ID = rm.ID limit 1));