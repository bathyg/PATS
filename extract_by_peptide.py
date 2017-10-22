from __future__ import print_function
import os, glob
from sys import argv, stderr
import time
from lz4framed import Compressor, Decompressor, Lz4FramedError, Lz4FramedNoDataError, get_block_size
import StringIO
import re
from pyteomics import mass
import cPickle as pickle
import bisect
from library import prolucid_search
from library import parameters
from library import translate
import argparse

def __error(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


def do_compress(in_stream, out_stream):
    read = in_stream.read
    read_size = get_block_size()
    try:
        with Compressor(out_stream) as compressor:
            try:
                while True:
                    compressor.update(read(read_size))
            # empty read result supplied to update()
            except Lz4FramedNoDataError:
                pass
            # input stream exception
            except EOFError:
                pass
    except Lz4FramedError as ex:
        __error('Compression error: %s' % ex)
        return 8
    return 0


def do_decompress(in_stream, out_stream):
    write = out_stream.write
    try:
        for chunk in Decompressor(in_stream):
            write(chunk)
    except Lz4FramedError as ex:
        __error('Compression error: %s' % ex)
        return 8
    return 0


def calculate_b_y_ion(sequence, ion_charge):
    aa_comp = dict(mass.std_aa_comp)
    aa_comp['C'] = mass.Composition({'H': 8, 'C': 5, 'S': 1, 'O': 2, 'N': 2})
    b_ion = [mass.calculate_mass(sequence[:aa], ion_type='b', charge=ion_charge, aa_comp=aa_comp) for aa in range(1, len(sequence))]  # aa = the amino acid residue
    y_ion = [mass.calculate_mass(sequence[aa:], ion_type='y', charge=ion_charge, aa_comp=aa_comp) for aa in range(1, len(sequence))]
    y_ion.reverse()  # record from small to big
    return (tuple(b_ion), tuple(y_ion))


def calculate_mass(sequence, charge):
    aa_comp = dict(mass.std_aa_comp)
    aa_comp['C'] = mass.Composition({'H': 8, 'C': 5, 'S': 1, 'O': 2, 'N': 2})
    return mass.calculate_mass(sequence, charge=charge, aa_comp=aa_comp)


def separate_ptm_seq(peptide_seq_with_ptm):
    s = peptide_seq_with_ptm
    ptm_list = []
    left = [m.start() for m in re.finditer('\(', s)]
    right = [m.start() for m in re.finditer('\)', s)]
    for idx, each_ptm in enumerate(left):
        ptm_list.append((int(left[idx] - 1), s[left[idx] - 1], float(s[left[idx] + 1:right[idx]])))
    regex = re.compile('[^a-zA-Z]')
    pep_seq = regex.sub('', s)
    return [ptm_list, pep_seq]


def extract_peptide(peptide_seq, mz4_folder, output_folder, result_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    os.chdir(mz4_folder)
    ptm_list, target_peptide = separate_ptm_seq(peptide_seq)  # [(3, 'Y', 79.9663), (18, 'C', -57.02146)]
    precursor_mass = calculate_mass(target_peptide, 1)
    for each_ptm in ptm_list:
        precursor_mass += each_ptm[2]
    precursor_mass_range = (precursor_mass * 0.999985, precursor_mass * 1.000015)
    print(precursor_mass_range)
    mass_index_list = pickle.load(open(os.path.join(mz4_folder, 'mass_index.p'), 'rb'))
    low_index = [i[0] for i in mass_index_list]
    high_index = [i[1] for i in mass_index_list]
    if precursor_mass_range[0] < mass_index_list[-1][0] and precursor_mass_range[1] > mass_index_list[0][0]:
        left_index = bisect.bisect_right(low_index, precursor_mass_range[0])
        right_index = bisect.bisect_left(high_index, precursor_mass_range[1])
        file_list = [i[2] for i in mass_index_list[left_index - 1:right_index + 1]]

    for idx, filename in enumerate(file_list):
        in_file = open(filename, 'rb')
        output_name = target_peptide + '_' + filename.replace('.mz4', '').replace('.', 'dot') + '.ms2'
        out_file = open(os.path.join(output_folder, output_name), 'wb')
        do_decompress(in_file, out_file)
        in_file.close()
        out_file.close()
    prolucid_search.search_extracted(output_folder, output_folder)
    translate.translate_sqt(glob.glob(os.path.join(output_folder, '*.sqt')), mz4_folder, result_file)


if __name__ == '__main__':
    start0 = time.clock()
    parser = argparse.ArgumentParser(description='Usage: python extract_by_peptide.py --peptide [your peptide sequence] --mz4_folder [folder to locate index files] --extract_folder [folder to store extracted ms2 files] --result_file [path and name of the result file]')
    parser.add_argument('--peptide', dest='peptide', help='your peptide sequence')
    parser.add_argument('--mz4_folder', dest='mz4_folder', help='absolute path to the folder to store indexed mass spectra')
    parser.add_argument('--extract_folder', dest='extract_folder', help='folder to store extracted ms2 files')
    parser.add_argument('--result_file', dest='result_file', help='path and name of the result file')
    results = parser.parse_args()

    extract_peptide(results.peptide, results.mz4_folder, results.extract_folder, results.result_file)

    #For example:
    #extract_peptide('RFDDAVVQSDMK', r'H:\example3\mz4', r'H:\example3\extract', r'H:\example3\result_RFDDAVVQSDMK.txt')
