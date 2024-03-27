from Bio import SeqIO
import os

def fragment_contigs(contigs_file_path, output_file_path, fragment_size=500):
    
    with open(contigs_file_path, 'r') as in_handle, open(output_file_path, 'w') as out_handle:
        for record in SeqIO.parse(in_handle, 'fasta'):
            num_fragments = len(record.seq) // fragment_size
            for i in range(num_fragments):
                start = i * fragment_size
                end = start + fragment_size
                fragment_seq = record.seq[start:end]
                fragment_id = f"{record.id}_fragment_{i+1}"
                fragment_record = record[start:end]
                fragment_record.id = fragment_id
                fragment_record.description = ''
                SeqIO.write(fragment_record, out_handle, 'fasta')

def process_all_samples(base_dir='spades_assembly', fragment_size=500):
    
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            sample_folder_path = os.path.join(root, dir_name)
            input_contigs_file = os.path.join(sample_folder_path, 'contigs.fasta')
            if os.path.exists(input_contigs_file):
                output_fragments_file = os.path.join(sample_folder_path, 'contig_fragments.fasta')
                fragment_contigs(input_contigs_file, output_fragments_file, fragment_size=fragment_size)
                print(f"Processed and fragmented contigs for {dir_name}")

fragment_size = 500  # Adjust value
process_all_samples(fragment_size=fragment_size)
