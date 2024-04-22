#This file will take the file paths from the SPAdes output in a soft-coded general manner and create a text file with the paths that wil be used by FastANI to calculate the
#similarities
import os

# Define the directory where the SPAdes assemblies are located
directory = "./spades_assembly/subsampling_output"

# List to store paths of contigs.fasta files
contigs_paths = []

# Traverse the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file is named contigs.fasta
        if file == "contigs.fasta":
            # Get the full path of the contigs.fasta file
            contigs_path = os.path.join(root, file)
            # Append the path to the list
            contigs_paths.append(contigs_path)

# Write the paths to a text file, one per line
output_file = "contigs_paths.txt"
with open(output_file, "w") as f:
    for path in contigs_paths:
        f.write(path + "\n")

print("Contigs paths written to:", output_file)
