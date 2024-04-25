import os

# Open the TSV file for reading
with open('fastani_output.tsv', 'r') as tsvfile:
    # Open a new file for writing the filtered data
    with open('filtered_file.tsv', 'w') as filtered_file:
        # Iterate through each line in the TSV file
        for line in tsvfile:
            # Split the line into columns
            columns = line.strip().split('\t')
            # Check if the value in the third column is not equal to 100
            if columns[2] != '100':
                # Write the line to the filtered file
                filtered_file.write(line)

# Define the SRR codes
srr_codes = ['SRR26772116', 'SRR26772099']

# Initialize dictionaries to store rows for each SRR code
srr_files = {srr_code: [] for srr_code in srr_codes}
mixed_file = []

# Open the filtered TSV file
with open('filtered_file.tsv', 'r') as tsvfile:
    # Iterate through each line in the file
    for line in tsvfile:
        # Split the line into columns
        columns = line.strip().split('\t')

        # Print the columns for debugging
        print("Columns:", columns)

        # Check if both columns start with 'SRR26772116'
        if all(column.startswith('SRR26772116') for column in columns[:2]):
            srr_files['SRR26772116'].append(line)
            print("Appending to SRR26772116")

        # Check if both columns start with 'SRR26772099'
        elif all(column.startswith('SRR26772099') for column in columns[:2]):
            srr_files['SRR26772099'].append(line)
            print("Appending to SRR26772099")

        # Check if either column starts with 'SRR26772099' or 'SRR26772116'
        elif any(column.startswith('SRR26772099') or column.startswith('SRR26772116') for column in columns[:2]):
            mixed_file.append(line)
            print("Appending to mixed")

# Debugging print statements
print("SRR26772116 lines:", len(srr_files['SRR26772116']))
print("SRR26772099 lines:", len(srr_files['SRR26772099']))
print("Mixed lines:", len(mixed_file))

# Write rows to separate files for each SRR code
for srr_code, rows in srr_files.items():
    with open(f'{srr_code}.tsv', 'w') as srr_file:
        srr_file.write(''.join(rows))

# Write rows to the mixed file
with open('mixed.tsv', 'w') as mixed_file_out:
    mixed_file_out.write(''.join(mixed_file))
