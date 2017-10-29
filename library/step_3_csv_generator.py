import cPickle as pickle
import parameters
import os


def check_dir_exist(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return 0


def step_3_generate_csv(uniprot_bait_dict, output_dir):
    string_score_dict = pickle.load(open(parameters.string_score, 'rb'))
    uniprot_string_dict = pickle.load(open(parameters.uniprot_string, "rb"))
    mouse_uniprot_to_gene = pickle.load(open(parameters.mouse_uniprot, "rb"))
    gene_to_human_uniprot = pickle.load(open(parameters.gene_to_human, "rb"))
    protein_bait_dict = pickle.load(open(uniprot_bait_dict, 'rb'))
    check_dir_exist(output_dir)
    os.chdir(output_dir)
    print "done loading"

    def uniprot_to_human(uniprotid):
        if uniprotid in mouse_uniprot_to_gene:
            gene_name = mouse_uniprot_to_gene[uniprotid]
            if gene_name.upper() in gene_to_human_uniprot:
                uniprotid = gene_to_human_uniprot[gene_name.upper()]
        return uniprotid

    def get_max_value(correlation_list):
        max_corr = 0.0
        for item in correlation_list:
            for each in item:
                try:
                    value_temp = float(each)
                except:
                    value_temp = 0
                if 1 > value_temp > max_corr:
                    max_corr = value_temp
        return max_corr

    def get_corr_from_gene(gene1, gene2):
        try:
            uniprot1 = gene_to_human_uniprot[gene1.upper()]
            uniprot2 = gene_to_human_uniprot[gene2.upper()]
        except:
            return 0
        if uniprot1 in uniprot_string_dict and uniprot2 in uniprot_string_dict:
            query_string = uniprot_string_dict[uniprot1] + uniprot_string_dict[uniprot2]
            if query_string in string_score_dict:
                corr_num_temp = string_score_dict[query_string]
                # print uniprot1, uniprot2, corr_num_temp
            else:
                corr_num_temp = 0
        else:
            corr_num_temp = 0
        return corr_num_temp

    def gen_csv(key):
        if 500 > len(protein_bait_dict[key]) > 1:
            correlation_list = []
            header_line = [gene_name for gene_name in protein_bait_dict[key]]
            header_line.insert(0, '      ')
            correlation_list.append(header_line)
            for each in protein_bait_dict[key]:
                line_temp = []
                line_temp.append(each)
                for every_entry in header_line[1:]:
                    if every_entry == each:
                        corr_string = str("%.4f" % 1.0)
                    else:
                        corr_string = str("%.4f" % get_corr_from_gene(each, every_entry))
                    line_temp.append(corr_string)
                correlation_list.append(line_temp)
            max_corr = get_max_value(correlation_list)
            filename = str(max_corr * 1000) + '_' + key + '.csv'
            with open(filename, 'wb') as file2:
                for line in correlation_list:
                    file2.writelines(','.join(line) + '\r\n')
        elif len(protein_bait_dict[key]) >= 500:
            filename = '0.1_' + key + '.csv'
            with open(filename, 'wb') as file2:
                file2.write('This protein was found in too many bait (%s in total) possibly a background protein.' % str(len(protein_bait_dict[key])))

    map(gen_csv, protein_bait_dict.keys())
    return 0


if __name__ == '__main__':
    step_3_generate_csv(parameters.uniprot_bait_dict, parameters.csv_dir)
