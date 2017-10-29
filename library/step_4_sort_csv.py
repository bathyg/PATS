# sort correlation values stored in csv with a header column and the a header row, assuming they are in the same order
import glob, os, shutil
import parameters
import cPickle as pickle
from sklearn.cluster import KMeans
from scipy.sparse import *
from math import sqrt
import multiprocessing

convert_all_to_human = 1


def check_dir_exist(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return 0


def uniprot_to_human(uniprotid):
    mouse_uniprot_to_gene = pickle.load(open(parameters.mouse_uniprot, "rb"))
    gene_to_human_uniprot = pickle.load(open(parameters.gene_to_human, "rb"))
    if uniprotid in mouse_uniprot_to_gene:
        gene_name = mouse_uniprot_to_gene[uniprotid]
        if gene_name.upper() in gene_to_human_uniprot:
            uniprotid = gene_to_human_uniprot[gene_name.upper()]
    return uniprotid


def read_file_from(filename):
    corr_array = []
    corr_num_array = []
    with open(filename) as file1:
        for line in file1:
            corr_array.append(line.strip().split(','))
    for each_line in corr_array[1:]:
        temp_array = [float(i) for i in each_line[1:]]
        corr_num_array.append(temp_array)
    return corr_array[0][1:], corr_num_array


def sort_table(protein_list, corr_list, kmean_maxk):
    if protein_list < 10:
        cluster_n = 2
    sorted_table = []
    cluster_n = int(sqrt(len(protein_list) / 2))
    if cluster_n > kmean_maxk:
        cluster_n = kmean_maxk
    if 5 < len(protein_list) < 10:
        cluster_n = 2
    elif len(protein_list) < 5:
        cluster_n = 1
    sparse_m = coo_matrix(corr_list)
    labeler = KMeans(n_clusters=cluster_n)
    labeler.fit(sparse_m.tocsr())
    num_ele = len(protein_list)
    sort_list = []
    for i in range(num_ele ** 2):
        y = i % num_ele
        x = (i - y) / num_ele
        if y >= x:
            corr_list[x][y] = 0
    for idx, each in enumerate(protein_list):
        sum_max = labeler.labels_[idx]
        sort_list.append((idx, sum_max))
    sorted_idx = [i[0] for i in sorted(sort_list, key=lambda x: x[1], reverse=True)]
    # print sorted_idx, protein_list
    header_line = [protein_list[i] for i in sorted_idx]
    header_line.insert(0, '      ')
    sorted_table.append(header_line)
    for x in sorted_idx:
        temp_list = []
        temp_list.append(protein_list[x])
        for y in sorted_idx:
            if x > y:
                temp_list.append("%.4f" % corr_list[x][y])
            elif y > x:
                temp_list.append("%.4f" % corr_list[y][x])
            else:
                temp_list.append('1.0000')
        sorted_table.append(temp_list)
    return sorted_table


def write_sorted(input_output_filename_tuple):
    input_file, output_file = input_output_filename_tuple
    convert_all_to_human = 0
    protein_list, number_list = read_file_from(input_file)
    if convert_all_to_human == 1:
        protein_list = [uniprot_to_human(i) for i in protein_list]
    filename_out = output_file
    if len(protein_list) > 5:
        sorted_table = sort_table(protein_list, number_list, 5)
        filename_out = output_file
        with open(filename_out, 'wb') as file2:
            for line in sorted_table:
                file2.writelines(','.join(line) + '\r\n')
    else:
        shutil.copy(input_file, filename_out)


def step_4_sort_csv(sort_input_dir, sort_output_dir):
    check_dir_exist(sort_output_dir)
    filename = []
    os.chdir(sort_input_dir)
    for csv_file in glob.glob("*.csv"):
        if not csv_file.startswith('0.'):
            filename.append((csv_file, os.path.join(sort_output_dir, os.path.basename(csv_file))))
        else:
            shutil.move(csv_file, sort_output_dir)
    os.chdir(sort_input_dir)
    pool = multiprocessing.Pool(processes=parameters.maximum_thread_number)
    pool.map(write_sorted, filename)
    pool.close()
    pool.join()


if __name__ == '__main__':
    step_4_sort_csv(parameters.csv_dir, parameters.sorted_csv_dir)
