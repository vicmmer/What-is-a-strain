from Bio import SeqIO
import os
import subprocess
import pandas as pd

# Define function to count reads in a fastq file
def count_reads(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file) // 4

# List to store input files for SPAdes
spades_input_files = []

# Iterate over each subsample
for file in os.listdir('.'):
    if 'subsample' in file and file.endswith('.fastq'):
        # For naming convention assuming the pair number 1 or 2 is right before ".fastq" and after "subsample"
        base_name = file.split('_subsample')[0]  
        pair_num = file.split('_')[-2] 
        
        # To construct the pair pattern for iteration
        if pair_num.endswith('1'):
            file2 = file.replace('_1_subsample', '_2_subsample')  
        else:
            continue  # To avoiding duplicated work
        
        # If the counterpart file actually exists
        if os.path.exists(file2):
            spades_input_files.extend([file, file2])
            # Count reads before and after filtering
            read_count = count_reads(file)
            with open('vic_spades.log', 'a') as log_file:
                sample_name = base_name.split('_')[0]  
                log_file.write(f"{sample_name} with subsample has {read_count} read pairs.\n")
    # Assemble each sample separately using SPAdes
output_folder_base = "spades_assembly"
k_mer_sizes = "77,99,127"
num_threads = 2

for i in range(0, len(spades_input_files), 2):
    file1 = spades_input_files[i]
    file2 = spades_input_files[i + 1]
    sample_name = file1.split('_')[0]  # Extract sample name from file1

    # Set up output folder for this sample
    output_folder = os.path.join(output_folder_base, sample_name)

    # Construct SPAdes command for this sample
    spades_command = f"spades.py -k {k_mer_sizes} -t {num_threads} --only-assembler"
    spades_command += f" -1 {file1} -2 {file2} -o {output_folder}"

    # Execute SPAdes command for this sample
    subprocess.run(spades_command, shell=True, check=True)

    # Write SPAdes command to log file
    with open('temp.log', 'a') as log_file:
        log_file.write(f"SPAdes assembly command for {sample_name}: {spades_command}\n")


# Function to filter contigs longer than 1000 bp
def filter_contigs(contigs_file_path, output_folder):
    filtered_contigs_file = os.path.join(output_folder, 'filtered_contigs.fasta')
    with open(contigs_file_path, 'r') as contigs_file, open(filtered_contigs_file, 'w') as filtered_file:
        for record in SeqIO.parse(contigs_file, 'fasta'):
            if len(record.seq) < 1000:
                SeqIO.write(record, filtered_file, 'fasta')
import os
from Bio import SeqIO

# Function to filter contigs longer than 1000 bp
def filter_contigs(contigs_file_path, output_folder):
    filtered_contigs_file = os.path.join(output_folder, 'filtered_contigs.fasta')
    with open(contigs_file_path, 'r') as contigs_file, open(filtered_contigs_file, 'w') as filtered_file:
        for record in SeqIO.parse(contigs_file, 'fasta'):
            if len(record.seq) < 1000:
                SeqIO.write(record, filtered_file, 'fasta')

# Specify the spades_assembly folder
spades_assembly_folder = 'spades_assembly'

# Iterate over each sample output folder dynamically
for root, dirs, files in os.walk(spades_assembly_folder):
    for dir_name in dirs:
        sample_folder_path = os.path.join(root, dir_name)
        contigs_file_path = os.path.join(sample_folder_path, 'contigs.fasta')
        if os.path.isfile(contigs_file_path):
            filter_contigs(contigs_file_path, sample_folder_path)
# Specify the spades_assembly folder
spades_assembly_folder = 'spades_assembly'

# Iterate over each sample output folder dynamically
for root, dirs, files in os.walk(spades_assembly_folder):
    for dir_name in dirs:
        sample_folder_path = os.path.join(root, dir_name)
        contigs_file_path = os.path.join(sample_folder_path, 'contigs.fasta')
        if os.path.isfile(contigs_file_path):
            filter_contigs(contigs_file_path, sample_folder_path)