# What-is-a-strain---Short-Read-Approach

Welcome to the "What is a strain" short read approach repository. 
Here, we will be showing a pipeline that begins with trimmed, raw microbial data in fastq format, and ends with creating output that is useful for diagnosing whether two samples are the same strain, providing statistical support for the likeliness of this case being so as well as density plot visuals, and an ANI threshold. 

Things will change as we go forward but for now, this is a description of the input files one can download by cloning this repository and the functionality of each script provided. 


## Input (downloadable by cloning this repository): 

### accessionList.txt
This list will contain the SRA accession number of the samples to be downloaded from NCBI, unless already provided by the user. 

### download_accessions.py 
This script automates the retrieval of sequencing data from the NCBI Sequence Read Archive (SRA) by running the fastq-dump command for each accession number listed in the accessionList.txt file, splitting the resulting files into forward and reverse reads if available.


### spades.py 
This script performs genome assembly using SPAdes for paired-end reads in FASTQ format. It iterates over each sample pair, counting read pairs before and after filtering, and logs this information. Afterwards,  it executes the filtering process for each sample dynamically by traversing through the spades_assembly folder and its subdirectories, and filtering out contigs shorter than 1,000 bp long, creating a new file within each subdirectory called "filtered_contigs.fasta" which will be used for further processing.

### fragmenting.py
This script loads the filtered contigs generated previously from the SPAdes assembly and processes them into smaller fragments (1000 base pairs). This is performed by using SeqIO.parse and by iterating over the sequences. The result is a new FASTA file where each original contig is represented by one or more fragments depending on its size.
