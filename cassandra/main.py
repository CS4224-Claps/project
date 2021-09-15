from cassandra.cluster import Cluster

# according to nodetool status here are the ips I have retrieved
# 192.168.48.255 ,192.168.51.0, 192.168.51.2, 192.168.51.1, 192.168.48.254

def main():
    cluster = Cluster(['192.168.48.255'])
    session = cluster.connect()

