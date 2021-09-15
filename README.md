# Project

Download dependencies: `pip install -r requirements.txt`

## `cockroachdb`

### Instructions

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

3.