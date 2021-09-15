from cassandra.cluster import Cluster


def main():
    cluster = Cluster(['192.168.48.255'])
    session = cluster.connect()

