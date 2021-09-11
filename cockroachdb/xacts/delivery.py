from datetime import datetime, timezone
import logging 

from utils.decorators import validate_command


@validate_command("D")
def execute(conn, io_line, data_lines=[]):
    # Retrieve Data from IO Line 
    w_id, carrier_id = map(int, io_line[1:])

    with conn.cursor() as cur:
        # (1) For d_id in [1, 10]:
        for d_id in range(1, 11):
            # (1a) Get smallest O_ID with (W_ID, D_ID) with O_CARRIER_ID IS NULL
            # (1b) Update Order by setting O_CARRIER_ID to CARRIER_ID 
            sql = """
                UPDATE Orders 
                    SET O_CARRIER_ID = %s
                    WHERE O_W_ID = %s AND O_D_ID = %s AND O_CARRIER_ID IS NULL 
                    ORDER BY O_ID ASC 
                    LIMIT 1
                    RETURNING O_ID, O_C_ID; 
            """

            cur.execute(sql, 
                (carrier_id, w_id, d_id)
            )
            row = cur.fetchone()
            o_id, c_id = row

            logging.debug("delivery: modifying %s %s", o_id, c_id)

            # (1c) Update all the order lines by setting OL_DELIVERY_D to now. 
            ol_delivery_d = str(datetime.now(timezone.utc))

            sql = """
                UPDATE OrderLine
                    SET OL_DELIVERY_D = %s 
                    WHERE OL_W_ID = %s AND OL_D_ID = %s AND OL_O_ID = %s
                    RETURNING OL_AMOUNT; 
            """

            cur.execute(sql, 
                (ol_delivery_d, w_id, d_id, o_id)
            )

            rows = cur.fetchall() 
            balance = sum(row[0] for row in rows)

            # (1d) Update C.BALANCE by B 
            sql = """
                UPDATE Customer
                    SET C_BALANCE = C_BALANCE + %s, 
                        C_DELIVERY_CNT = C_DELIVERY_CNT + 1
                    WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s; 
            """

            cur.execute(sql, 
                (balance, w_id, d_id, c_id)
            )

            logging.debug("delivery: status message: %s", cur.statusmessage)

    conn.commit()