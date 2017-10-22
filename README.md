# PATS, Post-acquisition targeted search (PATS)

* *Yu Gao, Jiao Ma, Alan Saghatelian, John R. Yates III @ The Scripps Research Institute & Salk Institute of Biological Studies*

## Purpose of this method:

PATS allows researchers to efficiently identify a peptide/protein of interest, with or without PTMs, from existing large mass spectrometry data sets. Using interactome data, PATS can assign putative functions of your target peptide/protein using known protein interactions.

### For example:

Researchers from lab X, identified a novel peptide "EDITPEP" with a novel PTM (+123.45 Da on E), and they want to know 

* *1. Is it real?*

* *2. Possible functions?*

**PATS solution:**
Go to sequest.scripps.edu/PATS, search for "E(+123.45)DITPE(+123.45)P" on PATS. If found, PATS will show the potential protein interaction network of it. If not found, PATS will allow you to submit it for search. After the search is done, PATS will email you and you will be able to see the search results.

**How it works?**
PATS is pre-loaded with two large interactome data sets [1](https://www.ncbi.nlm.nih.gov/pubmed/28514442) [2](https://www.ncbi.nlm.nih.gov/pubmed/26496610), containing more than 40,000 hours of AP-MS runs. Each AP-MS run contains mass spectrometry data of a pull-down experiment by a bait protein. PATS will search your target peptide with the novel PTM "E(+123.45)DITPE(+123.45)P" against all the data and see if it can be identified in any of 40,000 hours of AP-MS experiments. If your target is identified within multiple bait pull-downs, PATS will generate protein interaction network for your target peptide based on [STRING-DB](string-db.org).

## How to use PATS:

Here I will show three examples.

**Example 1 (easy)**
* *Target: Search a novel peptide from pre-loaded data sets.*

(1) Go to [PATS website](http://sequest.scripps.edu/PATS), search 'DVMLENYR', a tryptic peptide from Krüppel associated box (KRAB) domain.

(2) The results show all the gene/proteins containing this tryptic peptide 'DVMLENYR'. Note all the genes are ZNF， zinc finger proteins.

(3）Click gene name will direct you to the specific [gene card](http://www.genecards.org)

(4) Click protein name will direct you to the specific [uniprot entry](http://www.uniprot.org)

(5) Click network will direct you to the PATS generated protein interaction network, showing all the bait proteins in which 'DVMLENYR' can be identified. The proteins in the network are potential interactors of the gene/protein you clicked. Size of the circle is proportional to confidence and thickness of edges is proportional to STRING-DB score.

(6) Click correlation graph will direct you to the K-mean clustered protein correlation graph, showing all bait proteins related to DVMLENYR' and their STRING-DB correlation.

(7) Click Download correlation file will download a comma separated file (can be opened by Excel) for the correlation matrix.

(8) As seen in the PATS results, most of the proteins found are zinc-finger proteins, which are known to have KRAB domain.

**Example 2 (intermediate)**
* *Target: Search a novel protein with PTM from pre-loaded data sets.* *

(1) Go to [PATS website](http://sequest.scripps.edu/PATS), search tryptic peptide 'KVEEEQEADEEDVS(79.966331)EEEAESK', a known phosphorylation site on serine 247 in Human TMX1 protein. [Q9H3N1](http://www.uniprot.org/uniprot/Q9H3N1). 

(2) PATS will return not found and show the submission form.

(3) Fill the form with sequence "KVEEEQEADEEDVS(79.966331)EEEAESK", email "your email address" and click submit.

(4) Once finished, a link will be emailed to you with the search results.

(5) NOTE: Although PATS will take only seconds to extract a single peptide with PTM, the peptide database search may take a while. We use a job scheduler with limited computing resources and your submission will wait in a queue until all jobs (not only PATS jobs, also other jobs) submitted before finished running. In case we run out of resources and cannot fulfill your submission. We will send you a link to the extracted ms2 file. You can download the file and use your favorite search algorithm (SEQUEST, ProLuCID, etc.) to search it with your target sequence.

(6) Because of limited resources that we have, we do not provide automatic full protein sequence search now. If you want to search a protein or a list of proteins, please don't hesitate to contact me (ygao@scripps.edu) and we will see how can we help you on that.

**Example 3 (advanced)**
* *Target: Search peptide/proteins from my own raw data.* *

This will require you to install PATS on your own workstation/server. Please follow the installation guide at the bottom to install PATS and all dependencies.

MS2 files are in ***Example/ms2_files***

Files are downloaded from Bioplex and converted by Rawconverter to .ms2 file

To index the whole folder with all the ms2 files, run: 

```es6
python PATS_ms2_index.py --ms2_folder H:\example3\ms2_files --mz4_folder H:\example3\mz4 --max_thread_number 12
```
--ms2_folder specify where is the ms2 files located, use absolute path

--mz4_folder specify where the indexed mz4 files should be written, use absolute path

--max_thread_number specify how many threads you want to use. Here in this example we assume we have a 16 cores CPU and we use 12 threads

After running the PATS_ms2_index.py, a mz4 folder as specified in --mz4_folder will be created.

To find any specific peptide, we will use RFDDAVVQSDMK as an example here, run:
```es6
python extract_by_peptide.py --peptide RFDDAVVQSDMK --mz4_folder H:\example3\mz4 --extract_folder H:\example3\extract --result_file H:\example3\result_RFDDAVVQSDMK.txt
```
--peptide specify your peptide sequence

--mz4_folder specify folder to locate index files

--extract_folder specify folder to store extracted ms2 files 

--result_file specify path and name of the result file

After running the above command line, a file named H:\example3\result_RFDDAVVQSDMK.txt (as specified in --result_file) will be generated, and the content looks like the following:

```es6
Uniprot Name	Sequence count	Peptide sequence	Filename.Spectra_Number.Spectra_Numer.Charge	Bait Protein	XCorr	DeltaCN	Probability
tr|E9PPY6|E9PPY6_HUMAN	76	IGR.RFDDAVVQSDMK.HWP	cs_b3165_RAE1.8482.8482.2	1.8688	0.29296875	7.25223492727
tr|E9PPY6|E9PPY6_HUMAN	76	IGR.RFDDAVVQSDMK.HWP	cs_b3194_NHLRC2.7778.7778.2	3.2768	0.442230224609	10.8811000452
tr|E9PPY6|E9PPY6_HUMAN	76	IGR.RFDDAVVQSDMK.HWP	cs_b3268_HK3.8310.8310.2	4.6431	0.407378690961	9.75292364664
tr|E9PPY6|E9PPY6_HUMAN	76	IGR.RFDDAVVQSDMK.HWP	cs_b3165_RAE1.448.448.2	4.4632	0.385687399175	9.98165903916
tr|E9PPY6|E9PPY6_HUMAN	76	IGR.RFDDAVVQSDMK.HWP	cs_b3271_GFAP.9212.9212.3	2.4924	0.37421762157	8.1096894661
tr|E7ER27|E7ER27_HUMAN	68	GGK.AVANYDSVEEGEK.VVK	cs_b3268_HK3.6577.6577.2	2.6367	0.63310198354	11.5654076756
sp|Q9NRX4|PHP14_HUMAN	48	GYK.WAEYHADIYDK.VSG	cs_b3165_RAE1.15715.15715.3	1.2174	0.333744044685	4.43622046773
```


### Installation:

Dependency of PATS

Pyteomics https://pythonhosted.org/pyteomics/installation.html

Lz4framed https://pypi.python.org/pypi/py-lz4framed/0.9.7

numpy	http://www.numpy.org/

Use PATS to search a large data set downloaded from Pride. In this example, you will need proper resources for handling large data set. That includes fast (SSD, high IOPS) storage at least three times bigger than your target data set. If you want to search a data set with 500GB data, you should have at least 1.5 TB of free space on a fast storage. Otherwise, the speed of PATS will be disk-bound, instead of CPU-bound. 
(1) Download raw mass spectrometry data from Pride.
(2) Convert with your favorite converter from raw to ms2.
(3) Use "python PATS_ms2_index.py MS2_SOURCE_FOLDER INDEX_FILE_TEMP_FOLDER" to generate an index from the ms2 files in MS2_SOURCE_FOLDER and store in INDEX_FILE_TEMP_FOLDER


### How to cite:

Yu Gao, Jiao Ma, Alan Saghatelian, John R. Yates III, "TARGETED SEARCHES FOR NOVEL PEPTIDES IN BIG MASS SPECTROMETRY DATA SETS", submitted to Nature Methods
