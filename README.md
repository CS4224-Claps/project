# Project

## Prerequisites

1. The nodes can communicate with each other with passwordless ssh, i.e. you can do `ssh nodeB` from `nodeA` without any password.
One way to set this up is by running the following from `nodeA`.
```bash
ssh-keygen -t ed25519
cp ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```
2. CockroachDB and Cassandra is installed in your local node (`temp` folder) and they are accessible in your `PATH`. If that's not the case you can add this lines to `~/.bashrc`
```bash
export CASSANDRA_HOME=/temp/path/to/cassandra
export COCKROACHDB_HOME=/temp/path/to/cockroach/db
export PATH=$PATH:$CASSANDRA_HOME/bin:$COCKROACHDB_HOME
```
3. You are able to install python packages. We use [pyenv](https://github.com/pyenv/pyenv#basic-github-checkout).
4. Download dependencies by running `pip install -r requirements.txt`
5. The nodes has access to `nohup`
6. Set the configuration options following the example given in `config.json.example`. The name of the keys should be self-explanatory.
7. Make sure you are in one of the nodes (you might need to change the code manually if you mistakenly run this in a wrong node). Run `./setup.sh` once. This will create a HOSTNAME in the root folder.

## `cassandra`

### Database Setup

1. For each host, add the associated `cassandra.yaml` from the files in `cassandra/conf` 

For example, `cassandra-xcnd35.yaml` should belong under the server `xcnd35`, which should 
be located under the file `$CASSANDRA_HOME/conf/cassandra.yaml`. The same applies for the 
servers `xcnd36` to `xcnd39`. 

2. Once done, run `$CASSANDRA_HOME/bin/cassandra` 

Note: These are also under the assumption that you have set the alias for `CASSANDRA_HOME`
and that you have your 5 hosts setup, else the command would fail. 

Note: Alternativel, you can specify the configuration folder using: 
`$CASSANDRA_HOME/bin/cassandra -D cassandra.config=$CASSANDRA_HOME/conf`, where you specify 
the configuration folder above. 

### Seeding the database

1. Run `python cassandra/setup.py [--schema SCHEMA_FILE] [--seed SEED_DIR]`. By default, the schema files can be found at `cassandra/schema` folder

The following gives more information about the command line options for the cassandra setup script:

```
usage: setup.py [-h] [-c CONFIG_FILE] [--schema SCHEMA] [--seed SEED_DIR]

Parse input file and output file dest

optional arguments:
  -h, --help       show this help message and exit
  -c CONFIG_FILE   connection config file. defaults to config.json
  --schema SCHEMA  schema file to run (default to: cassandra/schema/schema.cql)
  --seed SEED_DIR  directory for seed file (default to: ../seed/data_files/)
```

It should take 5 - 10 minutes to setup the entire database. After this step, you can directly jump to the [Run experiments](#run-experiments) section.

## `cockroachdb`

### Database Setup

Please follow this [tutorial](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html) closely. We use the secure setup.

1. Run the following command: `bash cockroach-start.sh [HOSTS]`.
2. For example: `bash cockroach-start.sh xcnd35 xcnd36 xcnd37 xcnd38 xcnd39`

### Seeding the database

Prerequisite: You've run the one-time setup ( `./setup.sh` ). Look at the values stored in the file HOSTNAME in your root folder.

Assumptions:
1. A python file server is running inside your seed data folder at HOSTNAME. If that is not the case, change all occurrence of HOSTNAME in `cockroachdb/schema/schema*` to the fileserver hostname.
2. You are running an insecure node setup. If you are using a secure node setup, modify flags (e.g. `--certs-dir`) accordingly.

Note that the fileserver must be reachable by the node you are running the schema file from.

1. Start an http file server on HOSTNAME. `ssh HOSTNAME && cd [SEED_DIR] && python -m http.server 3000 &`
2. In any other node except HOSTNAME, run `cockroach sql --insecure --host $(hostname -s) --file [SCHEMA_FILE]`. By default, the schema files can be found at `cockroachdb/schema`

It should take 5 - 10 minutes to setup the entire database. After this step, you can directly jump to the [Run experiments](#run-experiments) section.

## Run experiments

The instructions below assume that the database are properly setup.

1. Seed the database. Follow the instructions for each database above.
2. Run `bash run.sh`. An interaction should look like the following.
```bash
$ bash run.sh
Found config.json... Please check if it is correct!
[config.json REDACTED]
Where is the project root located?
~/project
Which db are you using? (cassandra or cockroachdb)
cockroachdb
Please input 5 hostname separated by whitespace
xcnd35 xcnd36 xcnd37 xcnd38 xcnd39
Enter path to the workload you are running
~/seed/xact_files_A
```
3. The experiment logs would be available in `logs/dd-mm_HH-MM`. The `DBTYPE` file will indicate which db it is on.

## Performance

```
usage: main.py [-h] [-c CONFIG_FILE] -d DIRECTORY [-m MODE] [-s] [-x]

optional arguments:
  -h, --help      show this help message and exit
  -c CONFIG_FILE  config file. defaults to config.json
  -d DIRECTORY    directory containing xact logs
  -m MODE         mode to get cassandra or cockroach stats
  -s              flag to skip printing client and xact stats
  -x              flag to print xact summary stats
```

### Example Runs:

1. To get all the statistics with respect to cassandra: `python performance/main.py -d ./logs -m cassandra`
2. To get all the statistics with respect to cockroachdb: `python performance/main.py -d ./logs -m cockroach`
3. To get all the statistics with respect to cockroachdb, including xact summary stats, add the `-x` flag:
`python performance/main.py -d ./logs -m cockroach -x`
4. To simply print final values of cockroachdb, use the `-s` flag: `python performance/main.py -d ./logs -m cassandra -s`


## Misc

### Running the clients individually

If you would like to run just a single client:

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

### Running all clients in one node

- To run all clients in one node: `python run_clients.py --db cockroachdb -i ~/seed/xact_files_A -n 0 &`
