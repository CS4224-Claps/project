from cassandra import ConsistencyLevel
from cassandra.cluster import ExecutionProfile, Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.cluster import PreparedStatement, BoundStatement


def connect():
    contact_points = ['192.168.48.255', '192.168.51.0', '192.168.51.2', '192.168.51.1', '192.168.48.254']
    cluster_profile = ExecutionProfile(load_balancing_policy=RoundRobinPolicy(), consistency_level=ConsistencyLevel.QUORUM)
    cluster = Cluster(contact_points, execution_profiles={"profile": cluster_profile})
    session = cluster.connect()
    return session


def get_cassandra_stats(): 
    session = connect()

    warehouse_stats = session.prepare(
        """
        SELECT SUM(W_YTD)
            FROM wholesale.Warehouse;
        """
    )

    district_stats = session.prepare(
        """
        SELECT SUM(D_YTD), SUM(D_NEXT_O_ID)
            FROM wholesale.District; 
        """
    )

    customer_stats = session.prepare(
        """
        SELECT SUM(C_BALANCE), SUM(C_YTD_PAYMENT), SUM(C_PAYMENT_CNT), SUM(C_DELIVERY_CNT)
            FROM wholesale.Customer;
        """
    )

    order_stats = session.prepare(
        """
        SELECT MAX(O_ID), MAX(O_OL_CNT)
            FROM wholesale.Orders;
        """
    )

    orderline_stats = session.prepare(
        """
        SELECT SUM(OL_AMOUNT), SUM(OL_QUANTITY)
            FROM wholesale.OrderLine;
        """
    )

    stock_stats = session.prepare(
        """
        SELECT SUM(S_QUANTITY), SUM(S_YTD), SUM(S_ORDER_CNT), SUM(S_REMOTE_CNT)
            FROM wholesale.Stock;
        """
    )

    a = session.execute(warehouse_stats)
    print(a)
