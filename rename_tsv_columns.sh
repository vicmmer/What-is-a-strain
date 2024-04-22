# First, apply the second awk and redirect the output to a temporary file. This file will take the output file created from FastANI and make the columns more easily 
#interpreted 
awk '{
    sub("[^/]+/[^/]+/[^/]+/", "", $1);
    sub("[^/]+/[^/]+/[^/]+/", "", $2);
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5
}' fastani_output > temp_output.tsv

# Then, apply the first awk to the temporary file, output to try_output.tsv
awk '{
    sub("/.*", "", $1);
    sub("/.*", "", $2);
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5
}' temp_output.tsv > fastani_output.tsv

# Finally, delete the temporary file
rm temp_output.tsv
