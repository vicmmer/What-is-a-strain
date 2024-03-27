#COMP 383 
#Independent project
#Victoria, Adriana, Anmol, Ali

'''
This R script will incorporate th the statistical analysis implementation for 
our project, it will call upon a .tsv file that will be generated following our
ANI analysis and the fragmentation. Utilizing this string (and others like it)
we will compile them as a data frame and compare the dataframes to measure their
differences with one another (we want as low a p-value as possible to preserve
the diversity of our dataset)
'''
#begin implementation by importing/library-ing all necessary packages 
install.packages("tidyverse")
install.packages("readr")
library("readr")