from utils.decorators import validate_command, log_command


@validate_command("T")
@log_command
def execute(conn, io_line):    
    with conn.cursor() as cur:
        sql = """
            SELECT C_W_ID, C_D_ID, concact_wd(' ', C_FIRST, C_MIDDLE, C_LAST) AS C_NAME, C_BALANCE
                FROM Customer_Read NATURAL JOIN Customer_Write 
                ORDER BY C_BALANCE DESC 
                LIMIT 10; 
        """
        cur.execute(sql)
        customers = cur.fetchall()

        print("Customers: ")

        for customer in customers: 
            w_id, d_id, c_name, c_balance = customer     
                
            sql = """
                SELECT W_NAME 
                    FROM Warehouse_Read 
                    WHERE W_ID = %s;
            """
            
            cur.execute(sql)
            w_name, = cur.fetchone()

            sql = """
                SELECT D_NAME 
                    FROM District_Read 
                    WHERE D_W_ID = %s AND D_ID = %s;
            """
            cur.execute(sql)
            d_name = cur.fetchone()

            print(c_name, c_balance, w_name, d_name)

    conn.commit()

