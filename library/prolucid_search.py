import os, shutil, glob
import subprocess
import time
import parameters

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def run_prolucid(ms2_file):
    start=time.clock()
    java_exe = parameters.java_executable_path
    prolucid_jar_path=parameters.prolucid_jar
    RAM_per_prolucid=parameters.RAM_per_prolucid
    output_log_file = os.path.basename(ms2_file).replace('.ms2', '.log')
    print "Prolucid search started for %s" % ms2_file
    command_line = java_exe + ' -Xmx%s -jar %s %s search.xml %s' % (RAM_per_prolucid, prolucid_jar_path, ms2_file, parameters.maximum_thread_number)
    print command_line
    subprocess.Popen(command_line, stdout=open(output_log_file, 'wb')).communicate()
    output_sqt=os.path.basename(ms2_file).replace('.ms2', '.sqt')
    print "Search finished in %s (s)" % str(time.clock()-start)
    return output_sqt

def search_extracted(extract_dir, sqt_dir):
    if not os.path.exists(sqt_dir):
        os.makedirs(sqt_dir)
    os.chdir(extract_dir)
    file_list=glob.glob('*.ms2')
    search_xml='<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!--Parameters for ProLuCID database search-->\n<parameters>\n  <database>\n    <database_name>%s</database_name>\n    <is_indexed>false</is_indexed>\n  </database>\n  <search_mode>\n    <primary_score_type>1</primary_score_type>\n    <secondary_score_type>2</secondary_score_type>\n    <locus_type>1</locus_type>\n    <charge_disambiguation>0</charge_disambiguation>\n    <atomic_enrichement>0</atomic_enrichement>\n    <min_match>0</min_match>\n    <peak_rank_threshold>200</peak_rank_threshold>\n    <candidate_peptide_threshold>500</candidate_peptide_threshold>\n    <num_output>5</num_output>\n    <is_decharged>0</is_decharged>\n    <fragmentation_method>CID</fragmentation_method>\n    <multistage_activation_mode>0</multistage_activation_mode>\n    <preprocess>1</preprocess>\n  </search_mode>\n  <isotopes>\n    <precursor>mono</precursor>\n    <fragment>mono</fragment>\n    <num_peaks>1</num_peaks>\n  </isotopes>\n  <tolerance>\n    <precursor_high>3000.0</precursor_high>\n    <precursor_low>3000.0</precursor_low>\n    <precursor>25</precursor>\n    <fragment>100.0</fragment>\n  </tolerance>\n  <precursor_mass_limits>\n    <minimum>600.0</minimum>\n    <maximum>6000.0</maximum>\n  </precursor_mass_limits>\n  <precursor_charge_limits>\n    <minimum>0</minimum>\n    <maximum>1000</maximum>\n  </precursor_charge_limits>\n  <peptide_length_limits>\n    <minimum>6</minimum>\n  </peptide_length_limits>\n  <num_peak_limits>\n    <minimum>25</minimum>\n    <maximum>5000</maximum>\n  </num_peak_limits>\n  <max_num_diffmod>0</max_num_diffmod>\n  <modifications>\n    <display_mod>0</display_mod>\n    <n_term>\n      <static_mod>\n        <symbol>*</symbol>\n        <mass_shift>0.0</mass_shift>\n      </static_mod>\n      <diff_mods>\n        <diff_mod>\n          <symbol>*</symbol>\n          <mass_shift>0.0</mass_shift>\n        </diff_mod>\n      </diff_mods>\n    </n_term>\n    <c_term>\n      <static_mod>\n        <symbol>*</symbol>\n        <mass_shift>0.0</mass_shift>\n      </static_mod>\n      <diff_mods>\n        <diff_mod>\n          <symbol>*</symbol>\n          <mass_shift>0.0</mass_shift>\n        </diff_mod>\n      </diff_mods>\n    </c_term>\n    <static_mods>\n      <static_mod>\n        <symbol>*</symbol>\n        <mass_shift>57.02146</mass_shift>\n        <residue>C</residue>\n      </static_mod>\n    </static_mods>\n    <diff_mods />\n  </modifications>\n  <enzyme_info>\n    <name>trypsin</name>\n    <specificity>2</specificity>\n    <max_num_internal_mis_cleavage>2</max_num_internal_mis_cleavage>\n    <type>true</type>\n    <residues>\n      <residue>K</residue>\n      <residue>R</residue>\n    </residues>\n  </enzyme_info>\n</parameters>\n\n'%parameters.fasta_database_path
    with open('search.xml','wb') as search_xml_file:
        search_xml_file.write(search_xml)
    for each_ms2 in file_list:
        sqt_file=run_prolucid(each_ms2)
        shutil.move(sqt_file, os.path.join(sqt_dir,sqt_file))
        log_file=sqt_file.replace('.sqt','.log')
        shutil.move(log_file,os.path.join(sqt_dir,log_file))
    os.remove('search.xml')

if __name__=="__main__":
    search_extracted(r'H:\example3\extract',r'H:\example3\sqt')