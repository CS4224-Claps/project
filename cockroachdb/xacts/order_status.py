import logging

from utils.decorators import validate_command, log_command


@validate_command("O")
@log_command
def execute(conn, io_line):
    # Retrieve Data from IO Line
    w_id, d_id, c_id = map(int, io_line[1:])

    with conn.cursor() as cur:
        get_cust_info = """
            SELECT concat_ws(' ', C_FIRST, C_MIDDLE, C_LAST) as C_NAME, C_BALANCE
            FROM Customer
            WHERE C_W_ID = (%s) AND C_D_ID = (%s) AND C_ID = (%s)
        """
        cur.execute(get_cust_info, (w_id, d_id, c_id))
        c_name, c_balance = cur.fetchone()

        get_last_order = """
            SELECT O_ID, O_ENTRY_D, O_CARRIER_ID
            FROM Orders
            WHERE O_W_ID = (%s) AND O_D_ID = (%s) AND O_C_ID = (%s)
            ORDER BY O_ENTRY_D DESC
            LIMIT 1
        """
        cur.execute(get_last_order, (w_id, d_id, c_id))
        o_id, o_entry_d, o_carrier_id = cur.fetchone()

        get_order_items = """
            SELECT OL_I_ID, OL_SUPPLY_W_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D
            FROM OrderLine
            WHERE OL_W_ID = (%s) AND OL_D_ID = (%s) AND OL_O_ID = (%s)
        """
        cur.execute(get_order_items, (w_id, d_id, o_id))
        items = cur.fetchall()

        # Output the following information:
        print("1. Customer: ", c_name, c_balance)
        print("2. Last Order: ", o_id, o_entry_d, o_carrier_id)
        print("3. Items: ")

        for item in items:
            print(*item)

        logging.debug("order_status: status message: %s", cur.statusmessage)

    conn.commit()
