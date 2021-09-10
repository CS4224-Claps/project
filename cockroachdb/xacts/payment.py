import logging

from utils.decorators import validate_command


@validate_command("P")
def execute(conn, io_line):
    # Retrieve Data from IO Line
    _, w_id, d_id, c_id, pay_amt = io_line
    w_id, d_id, c_id, pay_amt = int(w_id), int(d_id), int(c_id), float(pay_amt)

    with conn.cursor() as cur:
        # (1) Update warehouse (W_ID)
        sql = """
            UPDATE Warehouse
                SET W_YTD = W_YTD + (%s)
                WHERE W_ID = (%s)
                RETURNING W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP
        """
        cur.execute(sql, (pay_amt, w_id))
        w_addr = cur.fetchone()

        # (2) Update district (W_ID, D_ID)
        sql = """
            UPDATE District
                SET D_YTD = D_YTD + (%s)
                WHERE D_W_ID = (%s) AND D_ID = (%s)
                RETURNING D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP
        """
        cur.execute(sql, (pay_amt, w_id, d_id))
        d_addr = cur.fetchone()

        # (3) Update customer (W_ID, D_ID, C_ID)
        sql = """
            UPDATE Customer
                SET C_BALANCE = C_BALANCE - (%s),
                C_YTD_PAYMENT = C_YTD_PAYMENT + (%s),
                C_PAYMENT_CNT = C_PAYMENT_CNT + 1
                WHERE C_W_ID = (%s) AND C_D_ID = (%s) AND C_ID = (%s)
                RETURNING *
        """
        cur.execute(sql, (pay_amt, pay_amt, w_id, d_id, c_id))
        cust = cur.fetchone()

        # (4) Output the following information:
        print("1. Customer info: ", cust)
        print("2. Warehouse address : ", w_addr)
        print("3. District address: ", d_addr)
        print("4. Payment amount: ", pay_amt)

        logging.debug("payment: status message: %s", cur.statusmessage)

    conn.commit()
