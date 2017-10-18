# PATS
Post-acquisition targeted search (PATS).

Yu Gao, Jiao Ma, Alan Saghatelian, John R. Yates III

The Scripps Research Institute
Salk Institute of Biological Studies

Purpose of this method:

Allows researchers to search large amount of mass spectrometry data for only a few peptide/protein of interest, with or without PTM.

How to use:

Here I will show three examples.

Example 1 (easy).
Search a novel peptide that I found from pre-loaded data. 



Example 3 (advanced).

Dependency of PATS

Pyteomics https://pythonhosted.org/pyteomics/installation.html
Lz4framed https://pypi.python.org/pypi/py-lz4framed/0.9.7
numpy	http://www.numpy.org/


Use PATS to search a large data set downloaded from Pride. In this example, you will need proper resources for handling large data set. That includes fast (ssd, high IOPS) storage at least three times bigger than your target data set. If you want to search a data set with 500GB data, you should have at least 1.5 TB of free space on a fast storage. Otherwise, speed of PATS will be disk-bound, instead of CPU-bound. 
(1) Download raw mass spectrometry data from Pride.
(2) Convert with your favaourite converter from raw to ms2.
(3) Use "python PATS_ms2_index.py MS2_SOURCE_FOLDER INDEX_FILE_TEMP_FOLDER" to generate index from the ms2 files in MS2_SOURCE_FOLDER and store in INDEX_FILE_TEMP_FOLDER


How to cite:

Yu Gao, Jiao Ma, Alan Saghatelian, John R. Yates III, "TARGETED SEARCHES FOR NOVEL PEPTIDES IN BIG MASS SPECTROMETRY DATA SETS", submitted to Nature Methods
