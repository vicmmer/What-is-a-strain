# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 15:32:27 2024

@author: anmol
"""

 #can try this first 
import fastani
fasta_file1 = #path to file
fasta_file2 = #path to file

result = fastani.run(fasta_file1, fasta_file2)

#or run this through os commands

#$ ./fastANI --ql [QUERY_LIST] --rl [REFERENCE_LIST] -o [OUTPUT_FILE]