import cPickle as pickle
import time
import glob
import os

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def read_translate_csv(filename):
    with open(filename, 'rb') as file_open:
        temp_array = [line.rstrip().split(',') for line in file_open]
    os.remove(filename)
    return temp_array

def generate_index(csv_folder,index_folder,num_split=1000):
    os.chdir(csv_folder)
    start = time.clock()
    csv_file_list = glob.glob('*.csv')
    file_list = sorted([(float(each_file.split('-')[0]), each_file) for each_file in csv_file_list],key=lambda x: x[0])

    #chunked_file_list=chunks(file_list,num_split)

    #for each_chunk in chunked_file_list:
    mass_translate_dict = {}
    min_mass=file_list[0][1].split('-')[0]
    max_mass=file_list[-1][1].split('-')[1].split('.csv')[0]
    dict_file_name='mass_spectra_no.index'
    dict_file_name=os.path.join(index_folder,dict_file_name)
    for each in file_list:
        temp = read_translate_csv(each[1])
        base_dir = os.path.dirname(temp[0][1])
        temp2 = [(int(i[0]), os.path.basename(i[1])) for i in temp]
        mass_translate_dict[each[1].replace('.csv', '')] = temp2

    pickle.dump(mass_translate_dict, open(dict_file_name, 'wb'), protocol=2)
