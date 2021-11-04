# Cassandra Project 

## Prerequisites 

1. The nodes can communicate with each other with passwordless ssh, 
i.e. you can do `ssh nodeB` from `nodeA` without any password.
One way to set this up is by running the following from `nodeA`.
```bash
ssh-keygen -t ed25519
cp ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```
2. CASSANDRA is installed in your local node (`temp` folder) and it is 
in your `PATH`. If that's not the case you can add this lines to `~/.bashrc`
```bash
export CASSANDRA_HOME=/temp/path/to/cassandra
export PATH=$PATH:$CASSANDRA_HOME/bin
```
3. You are able to install python packages. We use [pyenv](https://github.com/pyenv/pyenv#basic-github-checkout).
4. Download dependencies by running `pip install -r requirements.txt`
5. The nodes has access to `nohup`
6. Set the configuration options following the example given in `config.json.example`.

## Seeding the Database 

You would need to run the `setup.py` script in order to populate the database 
with the necessary data. 

1. `python cassandra/setup.py [--schema cassandra/schema/schema.cql] [--seed ~/seed/data_files/]`. 
(In brackets are the configuration options with its default values)

## Running the clients individually

1. Before running, ensure that you have the configuration file in the root
directory. An example of the configuration file can be found in `config.json.example`
2. To execute, run the command: `python cassandra/main.py -i <transaction file>`. More options can be seen below.

## Run experiment

1. Seed the database. Follow the instructions for each database above.
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
3. Please note that you must state that you are using **cassandra** as your db. 
4. The experiment logs would be available in `logs/dd-mm_HH-MM`. The `DBTYPE` file will indicate which db it is on.

## Performance

Once done, you should be able to use the performance code 
under `performance/main.py` to settle get the performance metrics. 

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

 To get all the statistics with respect to cassandra: `python performance/main.py -d ./logs -m cassandra`