from datetime import datetime, timezone
import logging 

from utils.decorators import validate_command


@validate_command("T")
def execute(conn, io_line, data_lines=[]):    
    with conn.cursor() as cur:
        sql = """
            SELECT C_W_ID, C_D_ID, C_FIRST, C_MIDDLE, C_LAST, C_BALANCE
                FROM Customer 
                ORDER BY C_BALANCE ASC 
                LIMIT 10;
        """

        cur.execute(sql)
        rows = cur.fetchall()

        for i in range(10):
            row = rows[i]
            w_id, d_id, c_first, c_middle, c_last, c_balance = row 

            sql = """
                SELECT W_NAME 
                    FROM Warehouse 
                    WHERE W_ID = %s;
            """
            cur.execute(sql, 
                (w_id, )
            )
            row = cur.fetchone()
            w_name = row[0]

            sql = """
                SELECT D_NAME 
                    FROM District 
                    WHERE D_W_ID = %s AND D_ID = %s;
            """
            cur.execute(sql, 
                (w_id, d_id)
            )
            row = cur.fetchone()
            d_name = row[0]        

            print("Customer: ", c_first, c_middle, c_last, 
                c_balance, w_name, d_name)   

    conn.commit()
