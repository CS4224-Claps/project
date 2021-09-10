from datetime import datetime, timezone
import logging 

from utils.decorators import validate_command


@validate_command("S")
def execute(conn, io_line, data_lines=[]):
    # Retrieve Data from IO Line 
    _, w_id, d_id, t, l = io_line
    
    with conn.cursor() as cur:
        # (1) Get D_NEXT_O_ID Given (W_ID, D_ID)
        sql = """
            SELECT D_NEXT_O_ID 
                FROM District 
                WHERE D_W_ID = %s AND D_ID = %s;
        """

        cur.execute(sql, 
            (w_id, d_id)
        )

        row = cur.fetchone()
        o_id = row[0]

        # (2) Get Items for the last L orders for district (W_ID, D_ID)
        sql = """
            SELECT OL_I_ID
                FROM OrderLine
                WHERE OL_W_ID = %s AND OL_D_ID = %s 
                    AND OL_O_ID >= %s - %s AND OL_O_ID < %s;
        """
        cur.execute(sql, 
            (w_id, d_id, o_id, l, o_id)
        )

        rows = cur.fetchall() 
        i_id_set = "(" + ",".join(str(row[0]) for row in rows) + ")"

        # (3) Output total # of items where S_QUANTITY < T        
        sql = """
            SELECT COUNT(*) 
                FROM Stock 
                WHERE S_W_ID = %s AND S_QUANTITY < %s
                    AND S_I_ID IN
        """

        cur.execute(sql + i_id_set, 
            (w_id, t)
        )

        row = cur.fetchone()
        count = row[0]

        print("Total Number of Items: ", count)

        logging.debug("stock: status message: %s", cur.statusmessage)


    conn.commit() 