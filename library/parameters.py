# Global parameters
java_executable_path = r'C:\Program Files\Java\jdk1.8.0_144\bin\java.exe'  # Where java.exe or java executable is

# prolucid search parameters
prolucid_jar = r'H:\PATS\library\ProLuCID1_3.jar'
fasta_database_path = r'H:\PATS\library\UniProt_Human_01-01-2017_reversed.fasta'  # Database for your search
maximum_thread_number = 12  # How many thread to use, minimum 8GB RAM and 1 cpu core is recommended per thread. For example, if you have 32GB RAM, use 4 threads maximum.
RAM_per_prolucid = '8G'  # How much memory for each prolucid process, recommend '8G' or '12G'

# DTASelect parameters
dta_select_result_dir = r'H:\mann_dta\sfp001'  # Where dta select output should be
DTASelect2_path = r'H:\PATS\library\DTASelect2'  # Where DTASelect2 folder is located
fdr_level = 'peptide'  # False discovery rate level, can be 'protein', 'peptide', or 'spectrum'.
fdr_threshold = 0.01  # False discovery threshold 0.01=1%
dta_peptide_per_protein = 1  # How many peptide per protein is required, default 1, may set to 2 to improve confidence
dta_tryptic_end_per_peptide = 2  # How many tryptic ends are required, 2 means both ends, 1 means at least 1 end, 0 means non tryptic peptide is allowed

# PATS running parameters
filename_bait_dict_csv = r'H:\mann_dta\sfp001\filename_bait_dict.csv'  # Filename-bait list
all_peptide = r'H:\mann_dta\sfp001\all_peptide.p'
uniprot_bait_dict = r'H:\mann_dta\sfp001\uniprot_bait_dict.p'
uniprot_bait_count_dict = r'H:\mann_dta\sfp001\uniprot_bait_count_dict.p'
csv_dir = r'H:\mann_dta\sfp001\output'
sorted_csv_dir = r'H:\mann_dta\sfp001\output\CSV'
plot_dir = r'H:\mann_dta\sfp001\output\GRAPH'
network_dir = r'H:\mann_dta\sfp001\output\NETWORK'
description_file = r'H:\mann_dta\sfp001\description.p'

# External databases
string_score = r'D:\Alan\CUFF\string_score.p'  # String-DB score database
uniprot_string = r'D:\Alan\CUFF\uniprot_string_dict2.p'  # UniprotID to String-DB identifier
mouse_uniprot = r'D:\Alan\CUFF\mouse_uniprot_to_gene.p'  # Mouse Uniprot to Gene
gene_to_human = r'D:\Alan\CUFF\gene_to_human_uniprot.p'  # Gene to Human Uniprot