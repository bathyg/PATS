import os, shutil, glob
import subprocess
from multiprocessing import Pool
import time
import parameters

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def run_file_list(file_list):
    result_dir = parameters.dta_select_result_dir
    java_exe = parameters.java_executable_path
    DTASelect2_path = parameters.DTASelect2_path
    peptide_per_protein = parameters.dta_peptide_per_protein  # p
    tryptic_ends_per_peptide = parameters.dta_tryptic_end_per_peptide  # y
    filter_level = {'peptide': '--sfp', 'protein': '--pfp', 'spectrum': '--fp'}
    fdr_level = parameters.fdr_level
    filter_fdr = parameters.fdr_threshold
    sequest_params='# comment lines begin with a \'#\' in the /first position\n[SEQUEST]\ndatabase_name = %s\npeptide_mass_tolerance = 3\ncreate_output_files = 1                ; 0=no, 1=yes\nion_series = 0 1 1 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0\nfragment_ion_tolerance = 0.0           ; leave at 0.0 unless you have real poor data\nnum_output_lines = 5                  ; # peptide results to show\nnum_description_lines = 3              ; # full protein descriptions to show for top N peptides\nshow_fragment_ions = 0                 ; 0=no, 1=yes\nprint_duplicate_references = 1         ; 0=no, 1=yes\nenzyme_number = 1\n#\n# Up to 3 differential searches can be performed.\n# Amino acids can not appear in more than one differential search parameter\n#\ndiff_search_options = 0.0 X 0.0 X 0.0 X\n#\n# new parameters\n#\nmax_num_differential_AA_per_mod = 4    ; max # of modified AA per diff. mod in a peptide\nnucleotide_reading_frame = 0           ; 0=proteinDB, 1-6, 7=forward three, 8=reverse three, 9=all six\nmass_type_parent = 0                   ; 0=average masses, 1=monoisotopic masses\nremove_precursor_peak = 0              ; 0=no, 1=yes\nmass_type_fragment = 1                 ; 0=average masses, 1=monoisotopic masses\nion_cutoff_percentage = 0.0            ; prelim. score cutoff %% as a decimal number i.e. 0.30 for 30%%\nmatch_peak_count = 0                   ; number of auto-detected peaks to try matching (max 5)\nmatch_peak_allowed_error = 1           ; number of allowed errors in matching auto-detected peaks\nmatch_peak_tolerance = 1.0             ; mass tolerance for matching auto-detected peaks\nmax_num_internal_cleavage_sites = 1    ; maximum value is 5; for enzyme search\n# partial sequence info ... overrides entries in .dta files\n#   up to 10 partial sequences ... each must appear in peptides\n#      analyzed in the forward or reverse directions\npartial_sequence =\n# protein mass & mass tolerance value i.e. 80000 10%%\n# or protein min & max value i.e. 72000 88000  (0 for both = unused)\nprotein_mass_filter = 0 0\n# For sequence_header_filter, enter up to five (5) strings where any one must\n# be in the header of a sequence entry for that entry to be searched.\n# Strings are space separated and \'~\' substitutes for a space within a string.\n# Example:  sequence_header_filter = human homo~sapien trypsin\nsequence_header_filter =\nadd_C_terminus = 0.0000                ; added to C-terminus (peptide mass & all Y-ions)\nadd_N_terminus = 0.0000                ; added to N-terminus (B-ions)\nadd_G_Glycine = 0.0000                 ; added to G - avg.  57.0519, mono.  57.02146\nadd_A_Alanine = 0.0000                 ; added to A - avg.  71.0788, mono.  71.03711\nadd_S_Serine = 0.0000                  ; added to S - avg.  87.0782, mono.  87.02303\nadd_P_Proline = 0.0000                 ; added to P - avg.  97.1167, mono.  97.05276\nadd_V_Valine = 0.0000                  ; added to V - avg.  99.1326, mono.  99.06841\nadd_T_Threonine = 0.0000               ; added to T - avg. 101.1051, mono. 101.04768\nadd_C_Cysteine = 57.02146              ; added to C - avg. 103.1388, mono. 103.00919\nadd_L_Leucine = 0.0000                 ; added to L - avg. 113.1594, mono. 113.08406\nadd_I_Isoleucine = 0.0000              ; added to I - avg. 113.1594, mono. 113.08406\nadd_X_LorI = 0.0000                    ; added to X - avg. 113.1594, mono. 113.08406\nadd_N_Asparagine = 0.0000              ; added to N - avg. 114.1038, mono. 114.04293\nadd_O_Ornithine = 0.0000               ; added to O - avg. 114.1472, mono  114.07931\nadd_B_avg_NandD = 0.0000               ; added to B - avg. 114.5962, mono. 114.53494\nadd_D_Aspartic_Acid = 0.0000           ; added to D - avg. 115.0886, mono. 115.02694\nadd_Q_Glutamine = 0.0000               ; added to Q - avg. 128.1307, mono. 128.05858\nadd_K_Lysine = 0.0000                  ; added to K - avg. 128.1741, mono. 128.09496\nadd_Z_avg_QandE = 0.0000               ; added to Z - avg. 128.6231, mono. 128.55059\nadd_E_Glutamic_Acid = 0.0000           ; added to E - avg. 129.1155, mono. 129.04259\nadd_M_Methionine = 0.0000              ; added to M - avg. 131.1926, mono. 131.04049\nadd_H_Histidine = 0.0000               ; added to H - avg. 137.1411, mono. 137.05891\nadd_F_Phenyalanine = 0.0000            ; added to F - avg. 147.1766, mono. 147.06841\nadd_R_Arginine = 0.0000                ; added to R - avg. 156.1875, mono. 156.10111\nadd_Y_Tyrosine = 0.0000                ; added to Y - avg. 163.1760, mono. 163.06333\nadd_W_Tryptophan = 0.0000              ; added to W - avg. 186.2132, mono. 186.07931\n#\n# SEQUEST_ENZYME_INFO _must_ be at the end of this parameters file\n#\n[SEQUEST_ENZYME_INFO]\n0.  No_Enzyme              0      -           -\n1.  Trypsin                1      KR          P\n2.  Chymotrypsin           1      FWY         P\n3.  Clostripain            1      R           -\n4.  Cyanogen_Bromide       1      M           -\n5.  IodosoBenzoate         1      W           -\n6.  Proline_Endopept       1      P           -\n7.  Staph_Protease         1      E           -\n8.  Trypsin_K              1      K           P\n9.  Trypsin_R              1      R           P\n10. AspN                   0      D           -\n11. Cymotryp/Modified      1      FWYL        P\n12. Elastase               1      ALIV        P\n13. Elastase/Tryp/Chymo    1      ALIVKRWFY   P' % parameters.fasta_database_path
    for each in file_list:
        temp_dir=os.path.basename(each)
        dta_name=temp_dir.replace('.sqt','.dta')
        os.mkdir(temp_dir)
        with open(os.path.join(temp_dir,'sequest.params'),'wb') as params_file:
            params_file.write(sequest_params)
        shutil.copy(each, temp_dir)
        temp_dir=os.path.join(result_dir,temp_dir)
        command_line=java_exe+' -cp '+DTASelect2_path+' DTASelect -p %s -y %s --trypstat %s %s --modstat --extra --pI --DB --dm -t 0 --brief --quiet'%(peptide_per_protein,tryptic_ends_per_peptide,filter_level[fdr_level],filter_fdr)
        subprocess.Popen(command_line, cwd=temp_dir, stdout=open(os.devnull, 'wb')).communicate()
        shutil.move(os.path.join(temp_dir,'DTASelect-filter.txt'),os.path.join(result_dir,dta_name))
        shutil.rmtree(temp_dir)
        print each,"done"

if __name__=='__main__':
    start=time.clock()
    result_dir=parameters.dta_select_result_dir
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    os.chdir(result_dir)
    exist_dta=glob.glob(os.path.join(result_dir,'*.dta'))
    sqt_input_dir=parameters.sqt_dir
    exist_dta_set=set([os.path.basename(i) for i in exist_dta])
    file_list=glob.glob(os.path.join(sqt_input_dir,'*.sqt'))
    file_list=[i for i in file_list if os.path.basename(i).replace('.sqt','.dta') not in exist_dta_set]
    job_list = list(chunks(file_list, len(file_list) / 100+1))


    #run_file_list(job_list[0])
    pool=Pool(processes=parameters.maximum_thread_number)
    pool.map(run_file_list, job_list)
    pool.close()
    pool.join()

    print "DTASelec2 finished, total time used:", time.clock()-start