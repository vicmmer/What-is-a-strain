import subprocess

def run_scripts():
    # Run subsample.py
    subprocess.run(['python', 'subsample.py'], check=True)

    # Run spades.py
    subprocess.run(['python', 'spades.py'], check=True)

    # Run getFilePaths.py
    subprocess.run(['python', 'getFilePaths.py'], check=True)

    # Run fastAni.py
    subprocess.run(['python', 'fastAni.py'], check=True)

    # Run rename_tsv_columns.py
    subprocess.run(['python', 'rename_tsv_columns.py'], check=True)

    # Run filter_tsv_file.py
    subprocess.run(['python', 'filter_tsv_file.py'], check=True)

if __name__ == "__main__":
    run_scripts()
