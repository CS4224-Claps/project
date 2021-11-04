from cassandra.cluster import PreparedStatement


def get_cassandra_stats(session):
    warehouse_stmt = session.prepare(
        """
        SELECT SUM(W_YTD)
            FROM wholesale.Warehouse;
        """
    )

    district_stmt = session.prepare(
        """
        SELECT SUM(D_YTD), SUM(D_NEXT_O_ID)
            FROM wholesale.District; 
        """
    )

    customer_stmt = session.prepare(
        """
        SELECT SUM(C_BALANCE), SUM(C_YTD_PAYMENT), SUM(C_PAYMENT_CNT), SUM(C_DELIVERY_CNT)
            FROM wholesale.Customer;
        """
    )

    order_stmt = session.prepare(
        """
        SELECT MAX(O_ID), MAX(O_OL_CNT)
            FROM wholesale.Orders;
        """
    )

    orderline_stmt = session.prepare(
        """
        SELECT SUM(OL_AMOUNT), SUM(OL_QUANTITY)
            FROM wholesale.OrderLine;
        """
    )

    stock_stmt = session.prepare(
        """
        SELECT SUM(S_QUANTITY), SUM(S_YTD), SUM(S_ORDER_CNT), SUM(S_REMOTE_CNT)
            FROM wholesale.Stock;
        """
    )

    w_ytd = session.execute(warehouse_stmt)[0][0]
    d_ytd, d_next_o_id = session.execute(district_stmt)[0]
    c_balance, c_ytd_payment, c_payment_cnt, c_delivery_cnt = session.execute(
        customer_stmt
    )[0]
    o_id, o_ol_cnt = session.execute(order_stmt)[0]
    ol_amount, ol_quantity = session.execute(
        orderline_stmt, execution_profile="profile"
    )[0]
    s_quantity, s_ytd, s_order_cnt, s_remote_cnt = session.execute(
        stock_stmt, execution_profile="profile"
    )[0]

    final_state = [
        w_ytd,
        d_ytd,
        d_next_o_id,
        c_balance,
        c_ytd_payment,
        c_payment_cnt,
        c_delivery_cnt,
        o_id,
        o_ol_cnt,
        ol_amount,
        ol_quantity,
        s_quantity,
        s_ytd,
        s_order_cnt,
        s_remote_cnt,
    ]

    print(final_state)

    return final_state
