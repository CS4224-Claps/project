#! /usr/bin/env bash

echo "Where is the project root located?"
read project_root

cd "$project_root"
(cd cockroachdb/schema && coc sql --file raw_init.sql)
python cockroachdb/postseed.py
