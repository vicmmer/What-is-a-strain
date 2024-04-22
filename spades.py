from Bio import SeqIO
import os
import subprocess

# Define function to count reads in a fastq file
def count_reads(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file) // 4

# List to store input files for SPAdes
spades_input_files = []

# Specify the directory where the FASTQ files are located
fastq_directory = 'subsampling_output'

# Iterate over each sample pair
for file1 in os.listdir(fastq_directory):
    if file1.endswith('_F.fastq'):
        file2 = file1.replace('_F.fastq', '_R.fastq')
        sample_name = file1[:-len('_F.fastq')]  # Extract entire base name
        # Add original FASTQ files to SPAdes input
        spades_input_files.extend([os.path.join(fastq_directory, file1), os.path.join(fastq_directory, file2)])
        # Count reads before and after filtering
        read_count = count_reads(os.path.join(fastq_directory, file1))
        with open('read_count.log', 'a') as log_file:
            log_file.write(f"{sample_name} has {read_count} read pairs.\n")

# Assemble each sample separately using SPAdes
k_mer_sizes = "77,99,127"
num_threads = 2

for i in range(0, len(spades_input_files), 2):
    file1 = spades_input_files[i]
    file2 = spades_input_files[i + 1]
    sample_name = file1[:-len('_F.fastq')]  # Extract entire base name

    # Set up output folder for this sample
    output_folder_base = os.path.join("spades_assembly", sample_name)  # Include sample_name in the output folder path

    # Ensure the output folder exists or create it
    if not os.path.exists(output_folder_base):
        os.makedirs(output_folder_base)

    # Construct SPAdes command for this sample
    spades_command = f"spades.py -k {k_mer_sizes} -t {num_threads} --only-assembler"
    spades_command += f" -1 {file1} -2 {file2} -o {output_folder_base}"

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

# Specify the spades_assembly folder
spades_assembly_folder = 'spades_assembly'

# Iterate over each sample output folder dynamically
for root, dirs, files in os.walk(spades_assembly_folder):
    for dir_name in dirs:
        sample_folder_path = os.path.join(root, dir_name)
        contigs_file_path = os.path.join(sample_folder_path, 'contigs.fasta')
        if os.path.isfile(contigs_file_path):
            filter_contigs(contigs_file_path, sample_folder_path)
