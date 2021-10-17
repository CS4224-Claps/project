from utils.decorators import validate_command, log_command


@validate_command("T")
@log_command
def execute(conn, io_line):    
    with conn.cursor() as cur:
        sql = """
            SELECT concat_ws(' ', c_first, c_middle, c_last) as c_name, c_balance, w_name, d_name
                FROM (Customer_Read NATURAL JOIN Customer_Write)
                INNER JOIN Warehouse_Read on w_id = c_w_id
                INNER JOIN District_Read on d_w_id = c_w_id and d_id = c_d_id
                WHERE (c_w_id, c_d_id, c_id) IN (
                    SELECT c_w_id, c_d_id, c_id 
                        FROM Customer_Write 
                        ORDER BY c_balance DESC 
                        LIMIT 10
                );
        """

        cur.execute(sql)
        customers = cur.fetchall()

        print("Customers: ")
        for customer in customers: 
            print(*customer)

    conn.commit()
