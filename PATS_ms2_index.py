import os, shutil, glob, sys
import argparse
import cPickle as pickle
import time
import math
from numpy import log
import multiprocessing
import lz4
import csv2index

def extract_idx(mass_pair):
    file_list = glob.glob(os.path.join(mass_pair[2], '*.idx'))
    index_spec = {}
    low_mass = mass_pair[0]
    high_mass = mass_pair[1]

    output_filename = 'index' + str(low_mass) + '_' + str(high_mass) + '.spec'
    output_filename = os.path.join(mass_pair[3],output_filename)
    for filename in file_list:
        list_temp = pickle.load(open(filename, 'rb'))
        list_temp = [i for i in list_temp if low_mass <= i[3] < high_mass]
        index_spec[filename.replace('.idx', '')] = list_temp
    pickle.dump(index_spec, open(os.path.join(mass_pair[2], output_filename), 'wb'), protocol=2)


def generate_mass_range_list(low, high, ppm_shift):
    increment = (1 + ppm_shift / 1000000.0)
    portions = int(log(high / low) / log(increment))
    mass_range_list = [low * math.pow(increment, i) for i in range(0, portions)]
    return mass_range_list


def write_translate_list(translate_list, translate_list_output):
    with open(translate_list_output, 'wb') as file1:
        for item in translate_list:
            file1.write(','.join(item) + '\n')


def extract_mass_to_file(file_pair):
    dict_index_file=file_pair[0]
    output_dir = file_pair[1]
    process_dir = file_pair[2]
    csv_dir = file_pair[3]
    split_index_file = dict_index_file.split('\\')[-1].split('_')
    low = float(split_index_file[0][5:])
    high = float(split_index_file[1][:-5])
    mass_range_list = generate_mass_range_list(low, high, 10)
    time1 = time.clock()
    dict_index = pickle.load(open(dict_index_file, 'rb'))
    #print 'time spent loading dict_index:', time.clock() - time1
    #print dict_index_file
    time1 = time.clock()

    for each_mass in mass_range_list:
        spectrum_idx = 1
        mass_high = each_mass * 1.00001
        mass_low = each_mass
        file_name_range=str(mass_low) + '-' + str(mass_high) + '.ms2'
        output_ms2 = os.path.join(output_dir,file_name_range)
        translate_list = []
        candid_list_dict = {}
        if not os.path.isfile(output_ms2):
            for key in dict_index:
                temp_list = [i for i in dict_index[key] if mass_low <= i[3] < mass_high]
                if len(temp_list) > 0:
                    candid_list_dict[key] = temp_list
            if len(candid_list_dict.keys()) > 0:
                output_file = open(output_ms2, 'ab')
                #print output_ms2
                output_file.write('H\tExtractor\tPATS\nH\tComments\tPATS by Yu (Tom) Gao 2017\nH\tFirstScan\t1\nH\tLastScan\t99999\n')

                for key in candid_list_dict:
                    key_filename = os.path.join(process_dir,os.path.basename(key)) + '.ms2'
                    ms2_file = open(key_filename, 'rb')
                    for item in candid_list_dict[key]:
                        ms2_file.seek(item[0])
                        content = ms2_file.read(item[1])
                        charge = item[4]
                        precursor_mass = (item[3] - 1.007276) / charge + 1.007276
                        original_idx = '.'.join([key, str(item[2]), str(item[2]), str(charge)])
                        translate_list.append((str(spectrum_idx), original_idx))
                        s_line = 'S\t%06d\t%06d\t%.5f\n' % (spectrum_idx, spectrum_idx, precursor_mass)
                        output_file.write(s_line)
                        z_line = 'Z\t%d\t%.5f\n' % (charge, item[3])
                        output_file.write(z_line)
                        output_file.write(content)
                        spectrum_idx += 1
                    ms2_file.close()
                output_file.close()

                write_translate_list(translate_list, os.path.join(csv_dir,os.path.basename(output_ms2).replace('ms2','csv')))


def Intensity(line):
    temp = line.split(' ')
    return float(temp[1])


def Mass(line):
    temp = line.split(' ')
    return float(temp[0])


def Combine_two_file(file1, file2, output):
    destination = open(output, 'wb')
    shutil.copyfileobj(open(file1, 'rb'), destination)
    shutil.copyfileobj(open(file2, 'rb'), destination)
    destination.close()


if __name__ == '__main__':

    start0 = time.clock()


    parser = argparse.ArgumentParser(description='Usage: python PATS_ms2_index.py --ms2_folder [your ms2 folder] --index_folder [folder to store index files]')
    parser.add_argument('--ms2_folder', dest='ms2_folder', help='absolute path to the folder of all source ms2 files')
    parser.add_argument('--mz4_folder', dest='mz4_folder', help='absolute path to the folder to store indexed mass spectra')
    parser.add_argument('--max_thread_number', dest='max_cpu', nargs='?', type=int, const=4, help='maximum number of thread used for indexing, default=4')

    results = parser.parse_args()
    print "Generating index files with %i threads..." % results.max_cpu
    index_folder = os.path.join(results.mz4_folder,'translate\\index\\')
    idx_folder = os.path.join(results.mz4_folder,'translate\\index\\idx\\')
    spec_folder = os.path.join(results.mz4_folder,'translate\\index\\spec\\')
    csv_folder = os.path.join(results.mz4_folder,'translate\\csv\\')
    ms2_folder = results.ms2_folder
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(spec_folder):
        os.makedirs(spec_folder)

    if not os.path.exists(idx_folder):
        os.makedirs(idx_folder)

    if not os.path.exists(index_folder):
        os.makedirs(index_folder)

    if not os.path.exists(results.mz4_folder):
        os.makedirs(results.mz4_folder)

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    process_dir = results.ms2_folder
    os.chdir(process_dir)
    file_list = glob.glob('*.ms2')
    if len(file_list) == 0:
        print "No ms2 file found at %s" % results.ms2_folder
    else:
        print "Total ms2 files: %s" % len(file_list)

    progress = 0
    offset = 0
    for filename in file_list:
        index_list = []
        file_split_all = open(filename, 'rb').read().split('\nS')
        header = file_split_all[0]
        offset = len(header) + 3
        spectra = file_split_all[1:]
        i = 0
        for spectrum in spectra:

            for idx, item in enumerate(spectrum):
                if item == 'Z':
                    before_z = idx + spectrum[idx:idx + 20].find('\n')
                    start_pos = offset + before_z
                    end_pos = len(spectrum) - before_z
                    index_list.append((start_pos, end_pos, int(spectrum[1:7].lstrip('0')), float(spectrum[idx:idx + 20].split('\n')[0].split('\t')[2]),
                                       int(spectrum[idx:idx + 20].split('\t')[1])))
                    # offset, length, index, precursor, charge
                    break
            offset += len(spectrum) + 2
        index_list = sorted(index_list, key=lambda x: x[3])
        pickle.dump(index_list, open(os.path.join(idx_folder, filename.replace('ms2', 'idx')), 'wb'), protocol=2)
        progress += 1

        if progress % 50 == 0:
            print progress, '/', len(file_list)
        del file_split_all

    print "Index finished in %.2f (s)" % (time.clock() - start0)
    start = time.clock()
    print "Generating spec files..."
    # index to spec

    list_mass = [(float(i), float(i + 200),idx_folder,spec_folder) for i in range(600, 6000, 200)]
    pool1 = multiprocessing.Pool(processes=results.max_cpu)
    pool1.map(extract_idx, list_mass)
    pool1.close()
    pool1.join()

    print "Spec file generated in %.2f (s)" % (time.clock() - start)
    start = time.clock()
    print "Generating MS2 files..."

    #generate indexed ms2
    file_list=glob.glob(os.path.join(spec_folder,'*.spec'))
    input_list=[(i,results.mz4_folder,ms2_folder, csv_folder) for i in file_list]


    pool2=multiprocessing.Pool(processes=results.max_cpu)
    pool2.map(extract_mass_to_file,input_list)
    pool2.close()
    pool2.join()
    #print generate_mass_range_list(850.0, 4500.0, 10)[0:20]
    #extract_mass_to_file(file_list[0])
    # yg_ms2_extract_single.extract_mass_to_file(process_dir, output_dir, 'C:\\gygi\\cs_mann\\index.spec', generate_mass_range_list(1235.0, 1236.0, 100))
    print "MS2 extracted in %.2f (s)" % (time.clock() - start)
    start = time.clock()
    print "Converting MS2 to MZ4 files..."

    os.chdir(results.mz4_folder)
    ms2_file_list=glob.glob('*.ms2')
    pool3=multiprocessing.Pool(processes=results.max_cpu)
    pool3.map(lz4.docomp, ms2_file_list)
    pool3.close()
    pool3.join()

    print "MZ4 file generated in %.2f (s)" % (time.clock() - start)
    start = time.clock()
    print "Generating index from csv..."
    csv2index.generate_index(csv_folder,index_folder,num_split=1000)

    print "Index file generated in %.2f (s)" % (time.clock() - start)
    start = time.clock()
    print "Indexing all finished in %.2f (s)" % (time.clock()-start0)

