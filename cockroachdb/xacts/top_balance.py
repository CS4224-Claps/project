from utils.decorators import validate_command, log_command


@validate_command("T")
@log_command
def execute(conn, io_line):
    with conn.cursor() as cur:
        cur.execute("SET TRANSACTION AS OF SYSTEM TIME '-30s'")

        sql = """
            SELECT concat_ws(' ', c_first, c_middle, c_last) as c_name, c_balance, w_name, d_name
                FROM Customer
                INNER JOIN Warehouse on w_id = c_w_id
                INNER JOIN District on d_w_id = c_w_id and d_id = c_d_id
                WHERE (c_w_id, c_d_id, c_id) IN (
                    SELECT c_w_id, c_d_id, c_id
                        FROM Customer
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
