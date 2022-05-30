# Host4Phage
Host4Phage is tool to type bacterial hosts for phages on the basis of genomic sequences of bacteriophages and bacteria. Host4Phage uses bacterial CRISPR-Cas system for this purpose. The tool supports multithreading.

## 1. Tools used by Host4phage
Host4phage uses other available tools: <br>

**PILER-CR** ---> [Reference](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-18) | [Source](https://www.drive5.com/pilercr/) <br>
**CRT** ---> [Reference](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-209) | [Source](http://www.room220.com/crt) <br>
**MinCED** --> [Source](https://github.com/ctSkennerton/minced) <br>
**CRISPRDetect** --> [Reference](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-016-2627-0) | [Source](https://github.com/ambarishbiswas/CRISPRDetect_2.2) <br>
**Kmer-db** --> [Reference](https://academic.oup.com/bioinformatics/article/35/1/133/5050791) | [Source](https://github.com/refresh-bio/kmer-db) <br>

All the above mentioned tools will be called from the tool/bin folder. 

## 2. Requirements
* To run host4phage.py you'll need Python 3.8.8 or greater.
* Python dependencies: `tqdm` --> `pip install tqdm` and `joblib` --> `pip install joblib`. Check out --> [tqdm](https://pypi.org/project/tqdm/)| [joblib](https://pypi.org/project/joblib/).
* CRT and MinCED tools require Java Runtime Environment. <br>
* CRISPRDetect tool requires the following tools: `clustalw` `water` `seqret` `RNAfold` `cd-hit-est` `blastn`.  Check out--> [CRISPRDetect](https://github.com/ambarishbiswas/CRISPRDetect_2.2).
* `FASTA` extension for input files is required --> `(*.fasta, *.fna, *.fa)`

## 3. Description and usage
The tool uses two subcommands: `spacers` and `compare`. 
* `spacers` subcommand is responsible for identifying and extracting *spacers*.
* `compare` subcommand is responsible for finding common sequences for hosts and bacteriophages by using *k*-mers. <br>

Host4Phage with `spacers` subcommand can be called from the command line in the following way (quick usage): <br>
`python  tool/host4phage.py spacers -i host_20_test -o output_spacers/piler -m piler` <br>

Host4Phage with `compare` subcommand can be called from the command line in the following way (quick usage): <br>
`python tool/host4phage.py compare  -s  output_spacers  -v  virus_20_test  -o  output_compare`<br> <br>

Parameters - `spacers` subcommand:

|Name|Requiredness|Description|
|----|----|----|
|`-input`/`-i`|obligatory|Directory path with bacterial genomes - files should <br> contain `FASTA` extension `(*.fasta, *.fna, *.fa)`.|
|`-method`/`-m`|obligatory|Method for CRISPR sequence identification <br> - `piler`/`crt`/`minced`/`crisprdetect`.|
|`-threads`/`-t`|optional|Number of threads - by default, is adjusted to the <br> number of processor threads in a user's computer.|
|`-output`/`-o`|optional|Directory path where two subdirectories will be created: <br> `output` containing result files of the selected method <br> and `fasta`  containing extracted *spacers* - by default, <br> the directory named `spacers` will be created.| <br> <br>
<br>

Parameters - `compare` subcommand:

Name|Requiredness|Description|
|----|----|----|
|`-spacers`/`-s`|obligatory|Directory path with extracted *spacers*  - if the directory <br> contains results from two or more methods for identifying <br> CRISPR sequences (e.g., the `output_spacers` directory will <br> contain subdirectories with *spacers*  for the CRT, MinCED, <br>  and PILER-CR program), you should pass the `output_spacers` <br> directory itself and the tool will combine the results of all <br>  the programs which are in it. You can also pass the paths separately <br>  to the results of each program in a single  command <br> to get the same result. Files with *spacers*  should be  in <br>`FASTA`  format `(*.fasta, *.fna, *.fa)`, because the tool <br> browses all subdirectories of the  specified  directory  to find <br>files with this format. |
|`-virus`/`-v`|obligatory|Directory path with bacteriophage genomes - files should <br> contain `FASTA` extension `(*.fasta, *.fna, *.fa)`|
|`-k`|optional|Length of *k*-mers - viral genomes and CRISPR spacers <br> found in hosts will be divided into sequences of that <br> length - by default, *k*=18. |
|`-threads`/`-t`|optional|Number of threads - by default, is adjusted to the  number <br> of processor threads in a user's computer.|
|`-output`/`-o`|optional| Directory path where a file with `.CSV` extension will be <br> created - by default, the directory will be named `comparison`.<br> The file will contain number of common *k*-mers of each <br>  bacterial and bacteriophage species.| <br> <br> <br>
<br>
<br>

You can also find the description of the parameters by using `python tool/host4phage.py --help`.


