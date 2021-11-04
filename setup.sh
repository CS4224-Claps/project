#! /usr/bin/env bash

# This file is a one-time setup to change all hardcoded hostname in files to your own choice

host=$(hostname -s)
echo "This is a one time setup... Changing all host placeholder -> $host"
echo "$host" > HOSTNAME && chmod -w HOSTNAME # will error on second run

sed -i "s|\\\$\\\$HOSTNAME\\\$\\\$|$host|" cassandra/utils/setup.py 2> /dev/null || true
sed -i "s|\\\$\\\$HOSTNAME\\\$\\\$|$host|" cockroachdb/schema/schema_*.sql 2> /dev/null || true
