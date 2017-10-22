import math
import cPickle as pickle
import os, glob
import parameters



def translate_sqt(sqt_list,mz4_dir,output_result):
    translate_dict=pickle.load(open(os.path.join(mz4_dir,r'translate\index\mass_spectra_no.index'),'rb'))
    file_output = open(output_result, 'wb')
    file_output.write('Uniprot Name\tSequence count\tPeptide sequence\tFilename.Spectra_Number.Spectra_Numer.Charge\tBait Protein\tXCorr\tDeltaCN\tProbability\r\n')
    for sqt_file in sqt_list:
        file_open = open(sqt_file, 'rb')
        sqt_split = file_open.read().split('\nS')
        trans_key=os.path.basename(sqt_file).split('_')[1].replace('dot','.').replace('.sqt','')
        file_open.close()
        trans_dict=dict(translate_dict[trans_key])
        for section in sqt_split[1:]:
            spec_no = int(section.split('\t')[1])
            M_sec = section.split('\nM')
            split_M = M_sec[1].split('\t')
            Xcorr1 = float(split_M[5])
            Prob = float(split_M[6])
            Xcorr2 = float(M_sec[2].split('\t')[5])
            if Xcorr1 != Xcorr2:
                DeltaCN = (Xcorr1 - Xcorr2) / Xcorr1
            else:
                DeltaCN = 0
            file_output.write(M_sec[1].split('\nL\t')[1].rstrip())
            file_output.write('\t')
            file_output.write(trans_dict[spec_no])
            file_output.write('\t')
            file_output.write('\t'.join(map(str, [Xcorr1, DeltaCN, Prob])))
            file_output.write('\r\n')
    file_output.close()

if __name__=="__main__":
    file_list=glob.glob(os.path.join(parameters.sqt_dir,'*.sqt'))
    translate_sqt(file_list,r'h:\example3\mz4',r'h:\example3\rr.txt')