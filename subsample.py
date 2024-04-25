import os
import random
import glob
from subprocess import check_output, run
from Bio import SeqIO

# Define function to count reads in a fastq file
def count_reads(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file) // 4

# Define function to filter contigs longer than 1000 bp
def filter_contigs(contigs_file_path, output_folder):
    filtered_contigs_file = os.path.join(output_folder, 'filtered_contigs.fasta')
    with open(contigs_file_path, 'r') as contigs_file, open(filtered_contigs_file, 'w') as filtered_file:
        for record in SeqIO.parse(contigs_file, 'fasta'):
            if len(record.seq) < 1000:
                SeqIO.write(record, filtered_file, 'fasta')

# For os function
path_in = os.getcwd()

# Define the path out as a folder called "subsampling_output" within the current directory
path_out = os.path.join(path_in, "subsampling_output")

# Create the output directory only if it doesn't exist
os.makedirs(path_out, exist_ok=True)

files = glob.glob(path_in + '/*')
a = [i for i in files if '.fastq' in i]
a.sort()

def wc(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])

print(files)

fi = 0
while fi < len(a) - 1:
    file1 = a[fi]
    file2 = a[fi+1]

    x = wc(file1)
    number_reads = int(x/4)
    random.seed(1)
    randomList = random.sample(range(0, number_reads), 5)
    counter = 1

    for i in randomList:
        sample_name1 = os.path.basename(file1).split('_')[0]
        sample_name2 = os.path.basename(file2).split('_')[0]

        output_file1 = f"{path_out}/{sample_name1}_sub{counter}_F.fastq"
        output_file2 =  f"{path_out}/{sample_name2}_sub{counter}_R.fastq" if file2 else None

        command = f'seqtk sample -s{i} {file1} 150000 > {output_file1}'
        run(command, shell=True, check=True)

        command = f'seqtk sample -s{i} {file2} 150000 > {output_file2}'
        run(command, shell=True, check=True)

        counter += 1
    fi += 2
