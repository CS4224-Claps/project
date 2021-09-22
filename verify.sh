#! /usr/bin/env bash

echo "Where are the output files located?"
read out_dir

echo "Where are the xact files located?"
read xact_dir 

_info="_info"

echo 'Starting Verification...'
echo

for i in {0..39}
do
    out_file="$out_dir/$i$_info.csv"
    out_num=$(eval "wc -l < $out_file")

    xact_file="$out_dir/$i.txt"
    xact_num=$(eval "grep -c '^[A-Za-z]' < $xact_file")

    if [[ $out_num -ne $xact_num ]]
    then 
        echo "FAILURE: Xact $i"
    fi
done 

echo 
echo 'Verification Complete.'
