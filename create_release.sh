#! /usr/bin/env bash

roll() {
    db=$1;
    target_dir="release/$db"
    mkdir -p $target_dir;
    cp -a $db performance $target_dir
    cp -a README.md setup.sh run.sh requirements.txt config.json.example run_clients.py $target_dir
    zip -r release/d.$db.zip $target_dir
}

rm -rf release/*
roll cassandra
roll cockroachdb


