import psycopg2


def get_cockroach_stats(dsn):
    conn = psycopg2.connect(dsn=dsn)
    final_state = []

    with conn.cursor() as cur:
        sqls = [
            """
            SELECT SUM(W_YTD)
                FROM Warehouse;
            """,
            """
            SELECT SUM(D_YTD), SUM(D_NEXT_O_ID)
                FROM District;
            """,
            """
            SELECT SUM(C_BALANCE), SUM(C_YTD_PAYMENT), SUM(C_PAYMENT_CNT), SUM(C_DELIVERY_CNT)
                FROM Customer;
            """,
            """
            SELECT MAX(O_ID), MAX(O_OL_CNT)
                FROM Orders;
            """,
            """
            SELECT SUM(OL_AMOUNT), SUM(OL_QUANTITY)
                FROM OrderLine;
            """,
            """
            SELECT SUM(S_QUANTITY), SUM(S_YTD), SUM(S_ORDER_CNT), SUM(S_REMOTE_CNT)
                FROM Stock;
            """,
        ]

        for sql in sqls:
            cur.execute(sql)
            final_state.extend(cur.fetchone())

    if len(final_state) != 15:
        raise ValueError("Final statistics missing values")

    return final_state
