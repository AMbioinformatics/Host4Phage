# Host4Phage
The Host4Phage tool is used to type bacterial hosts for phages based on the genomic sequences of bacteriophages and bacteria. Host4Phage uses the bacterial defense system CRISPR for this purpose. The tool supports multi-threaded computing and can therefore be run on both personal computers and high-performance computers. 

## 1. Tools used by Host4phage
Host4phage uses other available tools: <br>

**PILER-CR** ---> [Reference](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-18) | [Source](https://www.drive5.com/pilercr/) <br>
**CRT** ---> [Reference](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-209) | [Source](http://www.room220.com/crt) <br>
**MinCED** --> [Source](https://github.com/ctSkennerton/minced) <br>
**CRISPRDetect** --> [Reference](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-016-2627-0) | [Source](https://github.com/ambarishbiswas/CRISPRDetect_2.2) <br>
**Kmer-db** --> [Reference](https://academic.oup.com/bioinformatics/article/35/1/133/5050791) | [Source](https://github.com/refresh-bio/kmer-db) <br>

All the above mentioned tools are called from the tool/bin folder. 

## 2. Requirements
* To run host4phage.py you'll need Python 3.8.8 or greater.
* Python dependencies: `tqdm` --> `pip install tqdm` and `joblib` --> `pip install joblib`. Check out --> [tqdm](https://pypi.org/project/tqdm/) [joblib](https://pypi.org/project/joblib/).
* CRT and MinCED tools require Java Runtime Environment. <br>
* CRISPRDetect tool requires the following tools: `clustalw` `water` `seqret` `RNAfold` `cd-hit-est` `blastn`.  Check out--> [CRISPRDetect](https://github.com/ambarishbiswas/CRISPRDetect_2.2).
* Input files must have the `FASTA` extension --> `[*.fasta, *.fna, *.fa]`

## 3. Description
The tool uses two subcommands `spacers` and `compare`.  The `spacers` subcommand is responsible for identifying and extracting spacers, and the compare subcommand is responsible for finding common sequences for hosts and bacteriophages. <br>

Host4Phage with the `spacers` subcommand can be called from the command line in the following way: <br>
`python  tool/host4phage.py spacers -i host_20_test -o output_spacers/piler -m piler` <br>

Host4Phage with the `compare` subcommand can be called from the command line in the following way: <br>
`python tool/host4phage.py compare  -s  output_spacers  -v  virus_20_test  -o  output_compare`<br>


