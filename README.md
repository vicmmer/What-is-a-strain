# What-is-a-strain---Short-Read-Approach

Welcome to the "What is a strain" short read approach repository. 
Here, we will be showing a pipeline that begins with trimmed, raw microbial data in fastq format, and ends with creating output that is useful for diagnosing whether two samples are the same strain, providing statistical support for the likeliness of this case being so as well as density plot visuals, and an ANI threshold. 

The pipeline is broken into two parts:
  A) Python component: deals with the subsampling, spades assembly, calculating ANI similarity, and preparing a tsv file. 
  B) R component: takes the tsv file generated by Python as input to calculate density graphs of ANI similarities within strains, and even between strains. 


## PYTHON COMPONENT:

### accessionList.txt and download_accessions.py
This step is optional. These two scripts are used in tandem if user doesnt already have data (fastq files) downloaded unto the directory. 
a) accessionList.txt: This list will contain the SRA accession number of the samples to be downloaded from NCBI, unless already provided by the user. 
b) download_accessions.py : This script automates the retrieval of sequencing data from the NCBI Sequence Read Archive (SRA) by running the fastq-dump command for each accession number listed in the accessionList.txt file, splitting the resulting files into forward and reverse reads if available.

### Steps: 
Once the raw fastq files are found in the directory, follow these steps: 
**1. subsample.py** : Run this script to perform the subsampling. The input includes whatever fastq files are found in current directory. Output includes a folder called subsampling_output that contains the forward and reverse subsamples created from the oiriginal fastq files in the following format: Sample1_sub1_F.fastq & Sample1_sub1_R.fastq, Sample1_sub2_F.fastq & Sample1_sub2_R.fastq, etc up to however many subsamples were defined in the script: SampleN_subN_F.fastq & SampleN_subN_R.fastq

**2. spades.py** : Run this script to perform the spades assembly of the subsamples. The input includes all of the subsample pairs found in the /subsampling_output directory. Output includes a new folder /spades_assembly/subsampling_output which contains a folder for each subsample pair including the contigs.fasta needed for following step as well as other spades.output not used in this pipeline but available for extra information or debugging. 

**3. getFilePaths.py** : Run this script to get the complete path for all of the subsamples' contigs.fasta files which we will use for the ANI calculation. Output includes a contigs_paths.txt in the main directory that contains this information. 

**4. fastAni.py** : Run this script to perform a ANI comparison between all samples and subsamples' contig files. Input includes the contigs_paths.txt file created by step 3. Output includes the pairwise ANI comparison is a fastani_output file 

**5. rename_tsv_columns.sh** : run this script with ./rename_tsv_columns.sh to achieve two goals. First, it takes the fastani_output file anf turns it into a tsv file. Second, it filters the column names deleting the paths of the files used to create the ANI comparison, leaving only the subsample name, which makes it mroe readable for future visualization. 

**6. filter_tsv_file.py** : The tsv file created from fastAni needs some filtering as it includes entries that a) were comparisons between the same subsample yielding a result of 100, b)were comparisons between different strains. Therefore we want to make 3 different tsv files from the original tsv file. One tsv for SampleA only, one for SampleB only, and one for the comparisons between A and B. The output includes the tsv file for sampleA (SRR26772099.tsv), sampleB(SRR26772116.tsv) and between samples (mixed.tsv) 


## R COMPONENT: 

### StatAnalysisTentative.R
This R script focuses on analyzing Average Nucelotide Identity (ANI) data from a Lactobacillus gasseri bacterial species. The script starts by installing the necessary R packages for data manipulation and visualization. It defines a directory and reads multiple TSV files containing ANI data from that directory. The script then performs various statistical tests to analyze the data and these include, ANOVA, Shapiro-Wilk test for normality, Bartlett's test for homogeneity of variances, Kruskal-Wallis test, and Tukey's Honest Signiifcance Difference test to explore differences between bacterial strains. Additionally, it implements bootstrapping method to sample the data for further density estimation. The script also includes a permutation test to compare empirical data against the bootstrapped samples to validate the model and it concludes with generating a density plot of the ANI values using ggplot2 visually representing the statistical distribution and indicating signiifcant thresholds with vertical lines.






