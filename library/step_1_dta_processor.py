import glob, os
import parameters
import multiprocessing
import cPickle as pickle


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def read_bait_dict_from_csv(csv_filename):
    dict_temp = {}
    with open(csv_filename, 'rb') as csv_read:
        for line in csv_read:
            split_line = line.rstrip().split(',')
            filename = split_line[0]
            bait_gene = split_line[1]
            dict_temp[filename] = bait_gene
    return dict_temp


def read_peptide_from_files(file_chunk):
    peptide_list_temp = []
    uniprot_id = []
    peptide_line = 1
    peptide_spec_list = []
    filename_bait_dict = read_bait_dict_from_csv(parameters.filename_bait_dict_csv)
    filename_bait_dict_set = set(filename_bait_dict.keys())
    for each_file in file_chunk:
        with open(each_file, 'rb') as file_open:
            for line in file_open:
                split_line = line.split('\t')
                if len(split_line) > 3:
                    if split_line[0].startswith('sp|') or split_line[0].startswith('tr|'):
                        if peptide_line == 0:
                            uniprot_id.append(split_line[0].split('|')[1])
                        elif peptide_line == 1:
                            if len(uniprot_id) > 0:
                                peptide_list_temp.append((uniprot_id, peptide_spec_list))
                                uniprot_id = []
                                peptide_spec_list = []
                                uniprot_id.append(split_line[0].split('|')[1])
                            else:
                                uniprot_id.append(split_line[0].split('|')[1])
                            peptide_line = 0
                    elif len(split_line) == 15 and split_line[1].count('.') == 3:
                        unique_or_not = (split_line[0] == '*')
                        filename_bait = split_line[1].split('.')[0]
                        if filename_bait in filename_bait_dict_set:
                            bait_protein = filename_bait_dict[filename_bait]
                        else:
                            bait_protein = 'None'
                        sequence = split_line[-1].rstrip()[2:-2]
                        peptide_spec_list.append((unique_or_not, bait_protein, sequence))
                        peptide_line = 1
    return peptide_list_temp


def step_1_gen_all_peptide(all_peptide_filename):
    os.chdir(parameters.dta_select_result_dir)
    filename = glob.glob("*.dta")
    file_chunks = chunks(filename, int(len(filename) / parameters.maximum_thread_number + 1))
    pool = multiprocessing.Pool(processes=parameters.maximum_thread_number)
    peptide_list = pool.map(read_peptide_from_files, file_chunks)
    pool.close()
    pool.join()
    os.chdir(parameters.dta_select_result_dir)
    pickle.dump(peptide_list, open(all_peptide_filename, 'wb'), protocol=2)


if __name__ == '__main__':
    step_1_gen_all_peptide(parameters.all_peptide)
