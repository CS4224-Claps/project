#! /usr/bin/env bash

release_dir="group-d"

roll() {
    db=$1;
    target_dir="$release_dir/$db"
    mkdir -p $target_dir;
    cp -a $db performance $target_dir
    cp -a README.md setup.sh run.sh requirements.txt config.json.example run_clients.py $target_dir
    find group-d -type d -name __pycache__ -exec rm -fr {} \; # remove pycache
    zip -rq $release_dir/d.$db.zip $target_dir
}

rm -rf $release_dir/*
roll cassandra
roll cockroachdb


