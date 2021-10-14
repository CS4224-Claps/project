from cassandra import ConsistencyLevel
from cassandra.cluster import ExecutionProfile, Cluster
from cassandra.policies import RoundRobinPolicy


def connection():

    contact_points = ['192.168.48.255', '192.168.51.0', '192.168.51.2', '192.168.51.1', '192.168.48.254']
    cluster_profile = ExecutionProfile(load_balancing_policy=RoundRobinPolicy(), consistency_level=ConsistencyLevel.QUORUM)
    cluster = Cluster(contact_points, execution_profiles={"profile": cluster_profile})
    session = cluster.connect()

    return session