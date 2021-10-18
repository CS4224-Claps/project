from datetime import datetime, timezone
import logging

from utils.decorators import validate_command, log_command


@validate_command("N")
@log_command
def execute(conn, io_line, data_lines=[]):
    # Retrieve Data from IO Line
    c_id, w_id, d_id, num_items = map(int, io_line[1:])

    with conn.cursor() as cur:
        # (1) Retrieve D_NEXT_O_ID given (W_ID, D_ID)
        # (2) Update (W_ID, D_ID) by incrementing D_NEXT_O_ID by one
        sql = """
            UPDATE District
                SET D_NEXT_O_ID = D_NEXT_O_ID + 1
                WHERE D_W_ID = %s AND D_ID = %s
                RETURNING D_NEXT_O_ID - 1, D_TAX;
        """
        cur.execute(sql, (w_id, d_id))
        row = cur.fetchone()

        o_id, d_tax = int(row[0]), float(row[1])

        # (3) Create a new order
        o_all_local = 1
        for i in range(int(num_items)):
            _, supplier_warehouse, _ = data_lines[i]
            if supplier_warehouse != w_id:
                o_all_local = 0
                break

        o_entry_d = str(datetime.now(timezone.utc))

        sql = """
            INSERT INTO Orders
                (O_W_ID, O_D_ID, O_ID, O_C_ID,
                O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id; 
        """
        cur.execute(
            sql, (w_id, d_id, o_id, c_id, num_items, o_all_local, o_entry_d)
        )

        uuid, = cur.fetchone() 

        sql = """
            INSERT INTO Carrier VALUES (%s, %s);
        """
        cur.execute(
            sql, (uuid, None)
        )

        # (4) Initialize TOTAL_AMOUNT = 0
        total_amount = 0

        # (5) Create New Order-Lines
        ordered_items = []
        ordered_items_pretty = []

        for i in range(int(num_items)):
            item_number, supplier_warehouse, quantity = (
                int(data_lines[i][0]),
                int(data_lines[i][1]),
                float(data_lines[i][2]),
            )

            # (5a) Get S_QUANTITY
            # (5b) Set ADJUSTED_QTY
            # (5c) Set ADJUSTED_QTY += 100 IF ADJUSTED_QTY < 10
            # (5d) Update the stock record
            sql = """
                UPDATE Stock
                    SET S_QUANTITY = CASE
                        WHEN S_QUANTITY - %(qty)s < 10 THEN S_QUANTITY + 100 - %(qty)s
                        ELSE S_QUANTITY - %(qty)s
                    END,
                    S_YTD = S_YTD + %(qty)s,
                    S_ORDER_CNT = S_ORDER_CNT + 1,
                    S_REMOTE_CNT = CASE
                        WHEN %(supplier)s <> %(w_id)s THEN S_REMOTE_CNT + 1
                        ELSE S_REMOTE_CNT
                    END
                    WHERE S_W_ID = %(w_id)s AND S_I_ID = %(i_id)s
                    RETURNING S_QUANTITY;
            """
            cur.execute(
                sql,
                {
                    "qty": quantity,
                    "supplier": supplier_warehouse,
                    "w_id": w_id,
                    "i_id": item_number,
                },
            )
            row = cur.fetchone()
            adjusted_qty = float(row[0])

            # (5e) Update ITEM_AMOUNT
            sql = """
                SELECT I_NAME, I_PRICE
                    FROM Item
                    WHERE I_ID = %s;
            """
            cur.execute(sql, (item_number,))
            row = cur.fetchone()
            i_name, i_price = row[0], float(row[1])

            item_amount = quantity * i_price

            # (5f) Update TOTAL_AMOUNT
            total_amount += item_amount

            # (5g) Create new order-lines
            ordered_items.append(
                (
                    w_id,
                    d_id,
                    o_id,
                    i,
                    item_number,
                    None,
                    item_amount,
                    supplier_warehouse,
                    quantity,
                    "S_DIST_{:02d}".format(int(d_id)),
                )
            )

            # Append for output
            ordered_items_pretty.append(
                (
                    item_number,
                    i_name,
                    supplier_warehouse,
                    quantity,
                    item_amount,
                    adjusted_qty,
                )
            )

        # Add the new order-lines
        sql = """
            INSERT INTO OrderLine (OL_W_ID, OL_D_ID, OL_O_ID,
                OL_NUMBER, OL_I_ID, OL_DELIVERY_D, OL_AMOUNT,
                OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO)
                VALUES
        """

        items_values = ",".join(
            cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", item).decode("utf-8")
            for item in ordered_items
        )
        cur.execute(sql + items_values)

        # (6) Update TOTAL_AMOUNT
        sql = """
            SELECT W_TAX
                FROM Warehouse
                WHERE W_ID = %s;
        """
        cur.execute(sql, (w_id,))
        row = cur.fetchone()
        w_tax = float(row[0])

        sql = """
            SELECT C_DISCOUNT, C_LAST, C_CREDIT
                FROM Customer
                WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s;
        """
        cur.execute(sql, (w_id, d_id, c_id))
        row = cur.fetchone()
        c_discount, c_last, c_credit = float(row[0]), row[1], row[2]

        total_amount = total_amount * (1.0 + d_tax + w_tax) * (1.0 - c_discount)

        # (7) Output the following information:
        print("1. Customer: ", w_id, d_id, c_id, c_last, c_credit, c_discount)
        print("2. Warehouse: ", w_tax, d_tax)
        print("3. Order: ", o_id, o_entry_d)
        print("4. Items: ", num_items, round(total_amount, 2))
        print("5. Ordered Items: ")

        for ordered_item in ordered_items_pretty:
            print(ordered_item)

        logging.debug("new_order: status message: %s", cur.statusmessage)

    conn.commit()
