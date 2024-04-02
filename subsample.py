import os
import random
import glob
from subprocess import check_output

path_in = '/home/group6/What-is-a-strain---Short-Read-Approach-approach/'
path_out = '/home/group6/What-is-a-strain---Short-Read-Approach-approach/subsample_try/subsampling_output'

files = glob.glob(path_in + '*')
a = [i for i in files if '.fastq' in i]
a.sort()

def wc(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])

fi = 0
while fi < len(a):
    file1 = a[fi]
    file2 = a[fi+1]

    x = wc(file1)
    number_reads = int(x/4)
    random.seed(1)
    randomList = random.sample(range(0, number_reads), 50)
    counter = 1
    lpath = len(path_in)

    for i in randomList:
        command = f'seqtk sample -s{i} {file1} 150000 > {path_out}{counter}_{file1[lpath:]}'
        os.system(command)

        command = f'seqtk sample -s{i} {file2} 150000 > {path_out}{counter}_{file2[lpath:]}'
        os.system(command)

        counter += 1
    fi += 2
