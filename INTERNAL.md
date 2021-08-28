Several things to note:
1. The `ipaddrs` file contain the ip addresses of xcnd35 - xcnd39
2. The `/temp` folder is a local-to-node folder, meaning it is not replicated across xcnd35 - xcnd39

## Cassandra

- Cassandra is located at `echo $CASSANDRA_HOME`.
- xcnd35 is used as a seed node. So, the config file for this particular cassandra instance is a bit different than the other nodes. (`listen_address` is set to its IP)
- The Cassandra config is located at `conf/cassandra.yaml`
- Notable changes from default:
    - Change `num_tokens` from 16 -> 256

## CockroachDB

- CockroachDB is located at `echo $COCKROACHDB_HOME`
- The data lives under `data/` folder
- The logs lives under `data/logs` folder
- The certificates needed to make the cluster secure is under `certs`. One thing to note is the root certificate only exist in xcnd35. That's why you can only do `coc node status` from xcnd35.