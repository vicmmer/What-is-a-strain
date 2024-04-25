#!/bin/bash

# Run subsample.py
python subsample.py &&

# Run spades.py
python spades.py &&

# Run getFilePaths.py
python getFilePaths.py &&

# Run fastAni.py
python fastAni.py && 

# Run rename_tsv_columns.sh
./rename_tsv_columns.sh &&

# Run filter_tsv_file.py
python filter_tsv_file.py
