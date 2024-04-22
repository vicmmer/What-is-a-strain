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

fi = 0
while fi < len(a) - 1:
    file1 = a[fi]
    file2 = a[fi+1]

    x = wc(file1)
    number_reads = int(x/4)
    random.seed(1)
    randomList = random.sample(range(0, number_reads), 50)
    counter = 1

    for i in randomList:
        command = f'seqtk sample -s{i} {file1} 150000 > {path_out}/{counter}_{os.path.basename(file1)}'
        run(command, shell=True, check=True)

        command = f'seqtk sample -s{i} {file2} 150000 > {path_out}/{counter}_{os.path.basename(file2)}'
        run(command, shell=True, check=True)

        counter += 1
    fi += 2

# List to store input files for SPAdes
spades_input_files = []

# Iterate over each subsample
for file in os.listdir(path_out):
    if file.endswith('.fastq'):
        spades_input_files.append(os.path.join(path_out, file))

# Assemble each sample separately using SPAdes
output_folder_base = "spades_assembly"
k_mer_sizes = "77,99,127"
num_threads = 2

for i in range(0, len(spades_input_files), 2):
    file1 = spades_input_files[i]
    file2 = spades_input_files[i + 1]
    sample_name = os.path.basename(file1).split('_')[0]  # Extract sample name from file1

    # Set up output folder for this sample
    output_folder = os.path.join(output_folder_base, sample_name)

    # Construct SPAdes command for this sample
    spades_command = f"spades.py -k {k_mer_sizes} -t {num_threads} --only-assembler"
    spades_command += f" -1 {file1} -2 {file2} -o {output_folder}"

    # Execute SPAdes command for this sample
    run(spades_command, shell=True, check=True)

    # Write SPAdes command to log file
    with open('temp.log', 'a') as log_file:
        log_file.write(f"SPAdes assembly command for {sample_name}: {spades_command}\n")

# Filter contigs for each sample separately
spades_assembly_folder = 'spades_assembly'

for root, dirs, files in os.walk(spades_assembly_folder):
    for dir_name in dirs:
        sample_folder_path = os.path.join(root, dir_name)
        contigs_file_path = os.path.join(sample_folder_path, 'contigs.fasta')
        if os.path.isfile(contigs_file_path):
            filter_contigs(contigs_file_path, sample_folder_path)
