# Project

## Prerequisites

1. The nodes can communicate with each other with passwordless ssh, i.e. you can do `ssh nodeB` from `nodeA` without any password.
One way to set this up is by running the following from `nodeA`.
```bash
ssh-keygen -t ed25519
cp ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```
2. CockroachDB and CASSANDRA is installed in your local node (`temp` folder) and it is in your `PATH`. If that's not the case you can add this lines to `~/.bashrc`
```bash
export CASSANDRA_HOME=/temp/path/to/cassandra
export COCKROACHDB_HOME=/temp/path/to/cockroach/db
export PATH=$PATH:$CASSANDRA_HOME/bin:$COCKROACHDB_HOME
```
3. You are able to install python packages. We use [pyenv](https://github.com/pyenv/pyenv#basic-github-checkout).
4. Download dependencies by running `pip install -r requirements.txt`
5. The nodes has access to `nohup`

## `cockroachdb`

### Instructions

#### Seeding the database

1. Start an http file server on `xcnd36`. `ssh xcnd36 && cd seed && python -m http.server 3000`
2. In `xcnd35`, run `cd [project root]/cockroachdb/schema && coc sql --file raw_init.sql`

It should take ~ 5 minutes to setup the entire database.

#### Running the clients individually

1. Before running, ensure that you have the configuration file in the root
directory. An example of the configuration file can be found in `config.json.example`

2. To execute, run the command: `python cockroachdb/main.py -i <transaction file>`. More options can be seen below.

```
$ python cockroachdb/main.py -h
usage: main.py [-h] [-v] [-c CONFIG_FILE] [-i [INFILE]] [-o OUTDIR]

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   print debug info
  -c CONFIG_FILE  connection config file. defaults to config.json
  -i [INFILE]     input file containing xacts
  -o OUTDIR       output directory for logs
```

#### Running all clients in one node

- To run all clients in one node: `python run_clients.py --db cockroachdb -i ~/seed/xact_files_A -n 0 &`

#### Run experiments

1. Seed the database. Follow the instructions above
2. Run `bash run.sh`. An interaction should look like the following.
```bash
$ bash run.sh
Where is the project root located?
~/project
Which db are you using? (cassandra or cockroachdb)
cockroachdb
Which workload are you running? (A or B)
A
```
3. Run `python performance/main.py -d [log directory]`. Add `-x` flag to generate additional time stats for each transaction type.
4. Run `./verify.sh [out log directory] [xact_file directory]` to check if any of the client failed.
