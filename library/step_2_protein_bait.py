import cPickle as pickle
import parameters

def merge_two_dicts(x, y):
    z = {}
    for key in x:
        z[key] = 0
    for key in y:
        z[key] = 0
    for key in x:
        z[key] += x[key]
    for key in y:
        z[key] += y[key]
    return z

def read_bait_dict_from_csv(csv_filename):
    dict_temp={}
    with open(csv_filename,'rb') as csv_read:
        for line in csv_read:
            split_line=line.rstrip().split(',')
            filename=split_line[0]
            bait_gene=split_line[1]
            dict_temp[filename]=bait_gene
    return dict_temp

def step_2_generate_protein_bait(file_out, file_count_out, all_peptide):
    uniprot_bait_count_dict={}
    for each_list in all_peptide:
        for each_uniprot_list in each_list:
            uniprot_list=each_uniprot_list[0]
            peptide_list=each_uniprot_list[1]
            temp_dict={}
            for each_peptide in peptide_list:
                baitname=each_peptide[1]
                temp_dict[baitname]=0
            for each_peptide in peptide_list:
                baitname = each_peptide[1]
                temp_dict[baitname] +=1
            for each_uniprot in uniprot_list:
                if each_uniprot in uniprot_bait_count_dict:
                    uniprot_bait_count_dict[each_uniprot]=merge_two_dicts(uniprot_bait_count_dict[each_uniprot],temp_dict)
                else:
                    uniprot_bait_count_dict[each_uniprot]=temp_dict

    uniprot_bait_list_dict={}
    for uniprot in uniprot_bait_count_dict:
        uniprot_bait_list_dict[uniprot]=uniprot_bait_count_dict[uniprot].keys()

    pickle.dump(uniprot_bait_list_dict, open(file_out, 'wb'), protocol=2)
    pickle.dump(uniprot_bait_count_dict, open(file_count_out, 'wb'), protocol=2)

if __name__ == '__main__':
    all_peptide = pickle.load(open(parameters.all_peptide, 'rb'))
    file_out = parameters.uniprot_bait_dict
    file_count_out = parameters.uniprot_bait_count_dict
    step_2_generate_protein_bait(file_out,file_count_out,all_peptide)
