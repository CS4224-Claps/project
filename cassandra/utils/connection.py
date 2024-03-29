from cassandra import ConsistencyLevel
from cassandra.cluster import (
    ExecutionProfile,
    Cluster,
    EXEC_PROFILE_DEFAULT,
    RetryPolicy,
)
from cassandra.policies import RoundRobinPolicy, DowngradingConsistencyRetryPolicy


def connection(contact_points):

    # contact_points = ['192.168.48.255', '192.168.51.0', '192.168.51.2', '192.168.51.1', '192.168.48.254']
    cluster_profile = ExecutionProfile(
        load_balancing_policy=RoundRobinPolicy(),
        consistency_level=ConsistencyLevel.LOCAL_QUORUM,
        serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
        request_timeout=10000,
    )
    cluster = Cluster(
        contact_points, execution_profiles={EXEC_PROFILE_DEFAULT: cluster_profile}
    )
    session = cluster.connect()

    return session
