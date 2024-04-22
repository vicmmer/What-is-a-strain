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

### subsample_plus_assembly.py
This script automates the process of subsampling paired-end FASTQ files, which are commonly used in next-generation sequencing data analysis. The script begins by locating the input FASTQ files and specifying an output directory for the subsampled files. It then iterates through pairs of input files and calculates the number of reads in the first file. Using random sampling, it selects 50 random indices within the range of reads in the first file. This number of subsamples can be adjusted by the user based on their needs. For each index, it extracts a subset of reads from both files in the pair using the seqtk sample command and writes these subsampled reads to new files in the output directory. This process is repeated for each pair of input files, providing a convenient and automated way to generate subsampled datasets for downstream analysis or testing purposes. Following subsampling, SPAdes was used as a genome assembler to reconstruct genomic sequences from the subsampled reads, this captured the variability in the dataset and produced contigs.fasta files which later underwent filtering to remove contigs longer than 1000 base pairs. 

### StatAnalysisTentative.R
This R script focuses on analyzing Average Nucelotide Identity (ANI) data from a Lactobacillus gasseri bacterial species. The script starts by installing the necessary R packages for data manipulation and visualization. It defines a directory and reads multiple TSV files containing ANI data from that directory. The script then performs various statistical tests to analyze the data and these include, ANOVA, Shapiro-Wilk test for normality, Bartlett's test for homogeneity of variances, Kruskal-Wallis test, and Tukey's Honest Signiifcance Difference test to explore differences between bacterial strains. Additionally, it implements bootstrapping method to sample the data for further density estimation. The script also includes a permutation test to compare empirical data against the bootstrapped samples to validate the model and it concludes with generating a density plot of the ANI values using ggplot2 visually representing the statistical distribution and indicating signiifcant thresholds with vertical lines.


#test test



