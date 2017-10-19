# PATS, Post-acquisition targeted search (PATS)

* *Yu Gao, Jiao Ma, Alan Saghatelian, John R. Yates III @ The Scripps Research Institute & Salk Institute of Biological Studies* *

## Purpose of this method:

PATS allows researchers to efficiently identify a peptide/protein of interest, with or without PTMs, from existing large mass spectrometry data sets. Using interactome data, PATS can assign putative function of your target peptide/protein using known protein interaction.

For example, researchers from lab X identified a novel peptide "EDITPEP" with a novel PTM (+123.45 Da on E), and they want to know 1.If it is real? 2.Possible functions of it?

**PATS solution:**
Go to sequest.scripps.edu/PATS, search for "E(+123.45)DITPE(+123.45)P" on PATS. If found, PATS will show the potential protein interaction network of it. If not found, PATS will allow you to submit it for search. After the search is done, PATS will email you and you will be able to see the search results.

**How it works?**
PATS is pre-loaded with two large interactome data sets [1](https://www.ncbi.nlm.nih.gov/pubmed/28514442) [2](https://www.ncbi.nlm.nih.gov/pubmed/26496610), containing more than 40,000 hours of AP-MS runs. Each AP-MS run contains mass spectrometry data of a pull-down experiment by a bait protein. PATS will search your target peptide with the novel PTM "E(+123.45)DITPE(+123.45)P" against all the data and see if it can be identified in any of 40,000 hours of AP-MS experiments. If your target is identified within multiple bait pull-downs, PATS will generate protein interaction network for your target peptide based [STRING-DB](string-db.org).

## How to use:

Here I will show three examples.

**Example 1 (easy)**
* *Target: Search a novel peptide from pre-loaded data sets.* *

(1) Go to [PATS website](http://sequest.scripps.edu/PATS), search 'DVMLENYR', a tryptic peptide from Krüppel associated box (KRAB) domain.

(2) The results shows all the gene/proteins containing this tryptic peptide 'DVMLENYR'. Note all the genes are ZNF， zinc finger proteins.

(3）Click gene name will direct you to the specific [gene card](http://www.genecards.org)

(4) Click protein name will direct you to the specific [uniprot entry](http://www.uniprot.org)

(5) Click network will direct you to the PATS generated protein interaction network, showing all the bait proteins in which 'DVMLENYR' can be identified. The proteins in the network are potential interactors of the gene/protein you clicked. Size of the circle is proportional to confidence and thickness of edges is proportional to STRING-DB score.

(6) Click correlation graph will direct you to the K-mean clustered protein correlation graph, showing all bait proteins related to DVMLENYR' and their STRING-DB correlation.

(7) Click Download correlation file will download an comma separated file (can be opened by Excel) for the correlation matrix.

**Example 2 (intermediate)**
* *Target: Search a novel protein with PTM from pre-loaded data sets.* *


**Example 3 (advanced)**
* *Target: Search peptide/proteins from my own raw data.* *


This will require you to install PATS on your own workstation/server.

Installation:
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
