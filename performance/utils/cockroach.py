def get_cockroach_stats(conn):
    with conn.cursor() as cur:
        sql = """
            SELECT SUM(W_YTD)
                FROM Warehouse; 
        """

        cur.execute(sql)
        w_ytd, = cur.fetchone()

        sql = """
            SELECT SUM(D_YTD), SUM(D_NEXT_O_ID)
                FROM District; 
        """

        cur.execute(sql)
        d_ytd, d_next_o_id = cur.fetchone()

        sql ="""
            SELECT SUM(C_BALANCE), SUM(C_YTD_PAYMENT), 
                SUM(C_PAYMENT_CNT), SUM(C_DELIVERY_CNT)
                FROM Customer; 
        """

        cur.execute(sql)
        c_balance, c_ytd_payment, c_payment_cnt, c_delivery_cnt = cur.fetchone()

        sql = """
            SELECT MAX(O_ID), MAX(O_OL_CNT)
                FROM Orders; 
        """

        cur.execute(sql)
        o_id, o_ol_cnt = cur.fetchone()

        sql = """
            SELECT SUM(OL_AMOUNT), SUM(OL_QUANTITY)
                FROM OrderLine; 
        """

        cur.execute(sql)
        ol_amount, ol_quantity = cur.fetchone()

        sql = """
            SELECT SUM(S_QUANTITY), SUM(S_YTD), 
                SUM(S_ORDER_CNT), SUM(S_REMOTE_CNT)
                FROM Stock;
        """

        cur.execute(sql)
        s_quantity, s_ytd, s_order_cnt, s_remote_cnt = cur.fetchone()

        values = [w_ytd, d_ytd, d_next_o_id, c_balance, 
            c_ytd_payment, c_payment_cnt, c_delivery_cnt, 
            o_id, o_ol_cnt, ol_amount, ol_quantity, s_quantity, 
            s_ytd, s_order_cnt, s_remote_cnt]

        return [[v] for v in values]
