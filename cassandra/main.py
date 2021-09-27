from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.cluster import ExecutionProfile
from cassandra.policies import RoundRobinPolicy, RetryPolicy


# according to nodetool status here are the ips I have retrieved
# 192.168.48.255 ,192.168.51.0, 192.168.51.2, 192.168.51.1, 192.168.48.254

def main():
    retry_policy = RetryPolicy()
    cluster_profile = ExecutionProfile(load_balancing_policy=RoundRobinPolicy, consistency_level=ConsistencyLevel.QUORUM)
    cluster = Cluster(contact_points=['192.168.48.255', '192.168.51.0', '192.168.51.2', '192.168.51.1', '192.168.48.254'], execution_profiles=cluster_profile)
    session = cluster.connect()
    r = session.execute("SELECT * FROM system_schema.keyspaces;")
    print(r.current_rows)


if __name__ == "__main__":
    main()

