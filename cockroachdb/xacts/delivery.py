import logging

from utils.decorators import validate_command, log_command


@validate_command("D")
@log_command
def execute(conn, io_line):
    # Retrieve Data from IO Line
    w_id, carrier_id = map(int, io_line[1:])

    # (1) For d_id in [1, 10]:
    with conn.cursor() as cur:
        # (1a) Get smallest O_ID with (W_ID, D_ID) with O_CARRIER_ID IS NULL for all districts
        sql = """
            (SELECT O_D_ID, O_ID, O_C_ID
                FROM Orders
                WHERE O_W_ID = %s AND O_D_ID = %s AND O_CARRIER_ID IS NULL
                ORDER BY O_ID ASC
                LIMIT 1)
        """
        cur.execute(
            " UNION ALL ".join([sql] * 10),
            [
                i // 2 if i % 2 == 0 else w_id for i in range(1, 21)
            ],  # [w_id, 1, w_id, 2, ... ]
        )
        updated_orders = cur.fetchall()

        if updated_orders is None:
            logging.debug(f"no pending deliveries for w_id={w_id}! skipping ...")

        logging.debug(f"modifying {updated_orders}...")

        # (1b) Update Order by setting O_CARRIER_ID to CARRIER_ID for all districts
        sql = f"""
            UPDATE Orders
                SET O_CARRIER_ID = %s
                WHERE O_W_ID = %s
                    AND ({" OR ".join(["(O_D_ID = %s AND O_ID = %s AND O_C_ID = %s)"]*len(updated_orders))});
        """

        # combine res to fill in the OR clause
        params = [carrier_id, w_id]
        for order in updated_orders:
            params.extend(order)

        logging.debug(f"Updating orders with {params}")
        cur.execute(sql, params)

        for d_id, o_id, c_id in updated_orders:
            # for d_id in range(1, 11):
            # (1a) Get smallest O_ID with (W_ID, D_ID) with O_CARRIER_ID IS NULL
            # (1b) Update Order by setting O_CARRIER_ID to CARRIER_ID
            # sql = """
            #     UPDATE Orders
            #         SET O_CARRIER_ID = %s
            #         WHERE O_W_ID = %s AND O_D_ID = %s AND O_CARRIER_ID IS NULL
            #         ORDER BY O_ID ASC
            #         LIMIT 1
            #         RETURNING O_ID, O_C_ID;
            # """

            # cur.execute(sql, (carrier_id, w_id, d_id))
            # row = cur.fetchone()

            # if row is None:
            #     logging.debug(
            #         f"no pending deliveries for w_id={w_id}, d_id={d_id}! skipping..."
            #     )
            #     continue
            # o_id, c_id = row

            # logging.debug("delivery: modifying %s %s", o_id, c_id)

            # (1c) Update all the order lines by setting OL_DELIVERY_D to now.
            # ol_delivery_d = str(datetime.now(timezone.utc))

            # sql = """
            #     UPDATE OrderLine
            #         SET OL_DELIVERY_D = %s
            #         WHERE OL_W_ID = %s AND OL_D_ID = %s AND OL_O_ID = %s
            #         RETURNING OL_AMOUNT;
            # """

            # cur.execute(sql, (ol_delivery_d, w_id, d_id, o_id))

            # rows = cur.fetchall()
            # balance = sum(row[0] for row in rows)

            # (1d) Update C.BALANCE by B
            sql = """
                WITH balances AS (
                    UPDATE OrderLine
                        SET OL_DELIVERY_D = NOW()
                        WHERE OL_W_ID = %(w_id)s AND OL_D_ID = %(d_id)s AND OL_O_ID = %(o_id)s
                        RETURNING OL_AMOUNT
                )
                UPDATE Customer
                    SET C_BALANCE = C_BALANCE + (
                        SELECT SUM(OL_AMOUNT) FROM balances
                    ),
                        C_DELIVERY_CNT = C_DELIVERY_CNT + 1
                    WHERE C_W_ID = %(w_id)s AND C_D_ID = %(d_id)s AND C_ID = %(c_id)s;
            """

            cur.execute(
                sql,
                {
                    "w_id": w_id,
                    "d_id": d_id,
                    "c_id": c_id,
                    "o_id": o_id,
                },
            )

            logging.debug("delivery: status message: %s", cur.statusmessage)

        conn.commit()
