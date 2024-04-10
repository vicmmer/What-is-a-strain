import os
import random
import glob
from subprocess import check_output

#if hard-coding:
#path_in = '/home/group6/What-is-a-strain' 
#path_out = '/home/group6/What-is-a-strain/subsampling_output'

#Soft coding, estabishing path and output folder 
path_in = os.getcwd()
# Define path_out as a folder named "subsampling_output" within the current directory
path_out = os.path.join(path_in, "subsampling_output")

# Create the output directory if it doesn't exist
os.makedirs(path_out, exist_ok=True)

files = glob.glob(path_in + '/*')
a = [i for i in files if '.fastq' in i]
a.sort()

def wc(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])

fi = 0
while fi < len(a) - 1:
    file1 = a[fi]
    file2 = a[fi+1]

    x = wc(file1)
    number_reads = int(x/4)
    random.seed(1)
    randomList = random.sample(range(0, number_reads), 10)
    counter = 1
    lpath = len(path_in)

    for i in randomList:
        command = f'seqtk sample -s{i} {file1} 150000 > {path_out}/{counter}_{os.path.basename(file1)}'
        os.system(command)

        command = f'seqtk sample -s{i} {file2} 150000 > {path_out}/{counter}_{os.path.basename(file2)}'
        os.system(command)

        counter += 1
    fi += 2
