import subprocess

# Replace [QUERY_GENOME], [REFERENCE_LIST], and [OUTPUT_FILE] with your actual paths
query_genome = "./contigs_paths.txt"
reference_list = "./contigs_paths.txt"
output_file = "./fastani_output"

# Construct the command as a list of strings
command = ["fastANI", "--ql", query_genome, "--rl", reference_list, "-o", output_file]

# Execute the command
try:
    subprocess.run(command, check=True)
    print("Command executed successfully!")
except subprocess.CalledProcessError as e:
    print("Error executing command:", e)

