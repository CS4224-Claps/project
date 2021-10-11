#! /usr/bin/env bash

if [ $# -lt 2 ]; then
    echo "Usage: ./verify.sh out_dir xact_dir"
    return 1
fi

out_dir="$1"
xact_dir="$2"

_info="_info"

echo 'Starting Verification...'
echo

for i in {0..39}
do
    out_file="$out_dir/$i$_info.csv"
    out_num=$(eval "wc -l < $out_file")

    xact_file="$xact_dir/$i.txt"
    xact_num=$(eval "grep -c '^[A-Za-z]' < $xact_file")

    if [[ $out_num -ne $xact_num ]]
    then
        echo "FAILURE: Xact $i. Expected $xact_num, got $out_num"
    fi
done

echo
echo 'Verification Complete.'
