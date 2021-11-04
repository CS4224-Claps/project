from utils.decorators import validate_command, log_command


@validate_command("R")
@log_command
def execute(conn, io_line):
    # Retrieve Data from IO Line
    w_id, d_id, c_id = map(int, io_line[1:])

    with conn.cursor() as cur:
        cur.execute("SET TRANSACTION AS OF SYSTEM TIME '-30s'")

        get_related_customers = """
            SELECT o2.O_W_ID, o2.O_D_ID, o2.O_C_ID
            FROM Orders o1, Orders o2
            WHERE o1.O_W_ID = (%s) AND o1.O_D_ID = (%s) AND o1.O_C_ID = (%s) -- o1 is current customer's order
                AND o1.O_W_ID <> o2.O_W_ID
                AND EXISTS (
                    SELECT 1
                    FROM Orderline ol1, Orderline ol2, Orderline ol3, Orderline ol4
                    WHERE ol1.OL_W_ID = o1.O_W_ID AND ol1.OL_D_ID = o1.O_D_ID AND ol1.OL_O_ID = o1.O_ID -- ol1 = ol2
                        AND ol2.OL_W_ID = o2.O_W_ID AND ol2.OL_D_ID = o2.O_D_ID AND ol2.OL_O_ID = o2.O_ID
                        AND ol3.OL_W_ID = o1.O_W_ID AND ol3.OL_D_ID = o1.O_D_ID AND ol3.OL_O_ID = o1.O_ID -- ol3 = ol4
                        AND ol4.OL_W_ID = o2.O_W_ID AND ol4.OL_D_ID = o2.O_D_ID AND ol4.OL_O_ID = o2.O_ID
                        AND ol1.OL_I_ID <> ol3.OL_I_ID AND ol2.OL_I_ID <> ol4.OL_I_ID
                        AND ol1.OL_I_ID = ol2.OL_I_ID AND ol3.OL_I_ID = ol4.OL_I_ID
                )
        """
        cur.execute(get_related_customers, (w_id, d_id, c_id))
        related_customers = cur.fetchall()

    conn.commit()

    print("1. Customer: ", w_id, d_id, c_id)
    print("2. Related customers: ")
    for cust in related_customers:
        print(*cust)
