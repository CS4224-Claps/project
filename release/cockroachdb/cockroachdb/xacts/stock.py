import logging

from utils.decorators import validate_command, log_command


@validate_command("S")
@log_command
def execute(conn, io_line):
    # Retrieve Data from IO Line
    w_id, d_id, t, l = map(int, io_line[1:])

    with conn.cursor() as cur:
        cur.execute("SET TRANSACTION AS OF SYSTEM TIME '-30s'")

        # (1) Get D_NEXT_O_ID Given (W_ID, D_ID)
        sql = """
            SELECT D_NEXT_O_ID
                FROM District
                WHERE D_W_ID = %s AND D_ID = %s;
        """

        cur.execute(sql, (w_id, d_id))

        o_id = cur.fetchone()[0]

        # (2) Get Items for the last L orders for district (W_ID, D_ID) (In Subquery)
        # (3) Output total # of items where S_QUANTITY < T
        sql = """
            SELECT COUNT(*)
                FROM Stock
                WHERE S_W_ID = %s AND S_QUANTITY < %s
                    AND S_I_ID IN (
                        SELECT DISTINCT OL_I_ID
                            FROM OrderLine
                            WHERE OL_W_ID = %s AND OL_D_ID = %s
                                AND OL_O_ID >= %s - %s AND OL_O_ID < %s
                    );
        """

        cur.execute(sql, (w_id, t, w_id, d_id, o_id, l, o_id))

        low_stock_count = cur.fetchone()[0]
        print("Total Number of Items: ", low_stock_count)

        logging.debug("stock: status message: %s", cur.statusmessage)

    conn.commit()
