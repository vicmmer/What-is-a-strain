with open('fastani_output', 'r') as f:
    lines = f.readlines()

# First, apply the second awk and redirect the output to a temporary file
with open('temp_output.tsv', 'w') as temp_file:
    for line in lines:
        cols = line.strip().split('\t')
        cols[0] = cols[0].split('/')[-2]  # Extracts the second-to-last part of the path
        cols[1] = cols[1].split('/')[-2]  # Extracts the second-to-last part of the path
        temp_file.write('\t'.join(cols[:5]) + '\n')

# Then, apply the first awk to the temporary file, output to fastani_output.tsv
with open('temp_output.tsv', 'r') as temp_file:
    lines = temp_file.readlines()

with open('fastani_output.tsv', 'w') as output_file:
    for line in lines:
        cols = line.strip().split('\t')
        cols[0] = cols[0].split('/')[-1]  # Extracts the last part of the path
        cols[1] = cols[1].split('/')[-1]  # Extracts the last part of the path
        output_file.write('\t'.join(cols[:5]) + '\n')

# Finally, delete the temporary file
import os
os.remove('temp_output.tsv')



