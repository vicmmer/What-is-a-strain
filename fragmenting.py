from Bio import SeqIO
import os

def process_all_samples(base_dir='spades_assembly'):
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            sample_folder_path = os.path.join(root, dir_name)
            input_contigs_file = os.path.join(sample_folder_path, 'filtered_contigs.fasta')
            if os.path.exists(input_contigs_file):
                output_fragments_file = os.path.join(sample_folder_path, 'contig_fragments.fasta')
                with open(input_contigs_file, 'r') as in_handle, open(output_fragments_file, 'w') as out_handle:
                    contigs = SeqIO.parse(in_handle, 'fasta')
                    SeqIO.write(contigs, out_handle, 'fasta')
                print(f"Processed {dir_name}")

process_all_samples()
