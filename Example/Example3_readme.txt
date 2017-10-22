This is the file needed for example 3.

Simply create a folder on your disk, name it anything you like, for example we use C:\example

Download PATS source file from github.com/bathyg/PATS, put it in C:\PATS

Make sure you change all the paths in library/parameters.py

Specifically,

java_executable_path=r'C:\Program Files\Java\jdk1.8.0_144\bin\java.exe'     #Where java.exe or java executable is

#prolucid search parameters
prolucid_jar=r'C:\PATS\library\ProLuCID1_3.jar'
fasta_database_path=r'C:\PATS\library\UniProt_Human_01-01-2017_reversed.fasta'       #Database for your search
maximum_thread_number=4     #How many thread to use, minimum 8GB RAM and 1 cpu core is recommended per thread. For example, if you have 32GB RAM, use 4 threads maximum.
RAM_per_prolucid='8G'       #How much memory for each prolucid process, recommend '8G' or '12G'

#DTASelect parameters (no need if you don't run DTASelect with PATS)
dta_select_result_dir=r'C:\PATS\Example\dta'        #Where dta select output should be
DTASelect2_path = r'C:\PATS\library\DTASelect2'      #Where DTASelect2 folder is located
fdr_level = 'peptide'       #False discovery rate level, can be 'protein', 'peptide', or 'spectrum'.
fdr_threshold =0.01     #False discovery threshold 0.01=1%
dta_peptide_per_protein = 1     #How many peptide per protein is required, default 1, may set to 2 to improve confidence
dta_tryptic_end_per_peptide =2      #How many tryptic ends are required, 2 means both ends, 1 means at least 1 end, 0 means non tryptic peptide is allowed

After setting these up, you can follow the instruction on https://github.com/bathyg/PATS to run PATS

For any question about running PATS, please contact Yu (Tom) Gao, ygao@scripps.edu
