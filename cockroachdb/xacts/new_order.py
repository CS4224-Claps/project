from datetime import datetime, timezone
import logging 


SELECT_D_NEXT_O_ID_STMT = """
    SELECT D_NEXT_O_ID 
        FROM District 
        WHERE D_W_ID = %s AND D_ID = %s;
"""


UPDATE_D_NEXT_O_ID_STMT = """
    UPDATE District 
        SET D_NEXT_O_ID = %s 
        WHERE D_W_ID = %s AND D_ID = %s;
"""


INSERT_NEW_ORDER_STMT = """
    INSERT INTO Orders 
        (O_W_ID, O_D_ID, O_ID, O_C_ID, O_CARRIER_ID, 
        O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

SELECT_STOCK_QUANTITY_STMT = """
    SELECT S_QUANTITY 
        FROM Stock 
        WHERE S_W_ID = %s AND S_I_ID = %s;
"""


UPDATE_STOCK_QUANTITY_STMT = """
    UPDATE Stock 
        SET S_QUANTITY = %s, 
            S_YTD = S_YTD + %s, 
            S_ORDER_CNT = S_ORDER_CNT + 1
        WHERE S_W_ID = %s AND S_I_ID = %s; 
"""


UPDATE_STOCK_REMOTE_CNT_STMT = """
    UPDATE Stock 
        SET S_REMOTE_CNT = S_REMOTE_CNT + 1, 
        WHERE S_W_ID = %s AND S_I_ID = %s; 
"""


SELECT_ITEM_NAME_PRICE_STMT = """
    SELECT I_NAME, I_PRICE 
        FROM Item 
        WHERE I_ID = %s; 
"""


INSERT_NEW_ORDER_LINE_STMT = """
    INSERT INTO OrderLine (OL_W_ID, OL_D_ID, OL_O_ID, 
        OL_NUMBER, OL_I_ID, OL_DELIVERY_D, OL_AMOUNT, 
        OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""


SELECT_DISTRICT_TAX_STMT = """
    SELECT D_TAX 
        FROM District 
        WHERE D_W_ID = %s AND D_ID = %s;
"""


SELECT_WAREHOUSE_TAX_STMT = """
    SELECT W_TAX 
        FROM Warehouse 
        WHERE W_ID = %s; 
"""


SELECT_CUSTOMER_DISCOUNT_STMT = """
    SELECT C_DISCOUNT 
        FROM Customer 
        WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s; 
"""


SELECT_CUSTOMER_LAST_CREDIT_STMT = """
    SELECT C_LAST, C_CREDIT 
        FROM Customer 
        WHERE C_W_ID = %s AND C_D_ID = %s AND C_ID = %s; 
"""


def execute(conn, io_line, data_lines=[]):
    # Retrieve Data from IO Line 
    _, w_id, d_id, c_id, num_items = io_line
    
    with conn.cursor() as cur:
        # (1) Retrieve D_NEXT_O_ID given (W_ID, D_ID) 
        cur.execute(SELECT_D_NEXT_O_ID_STMT, 
            (w_id, d_id)
        )
        rows = cur.fetchone()
        d_next_o_id = rows[0]

        # (2) Update (W_ID, D_ID) by incrementing D_NEXT_O_ID by one 
        cur.execute(UPDATE_D_NEXT_O_ID_STMT, 
            (d_next_o_id, w_id, d_id)
        )

        # (3) Create a new order 
        o_all_local = 1
        for i in range(int(num_items)):
            _, supplier_warehouse, _ = data_lines[i]
            if supplier_warehouse != w_id: 
                o_all_local = 0
                break

        o_entry_d = str(datetime.now(timezone.utc))
        cur.execute(INSERT_NEW_ORDER_STMT, 
            (
                w_id, 
                d_id, 
                d_next_o_id, 
                c_id, 
                None, 
                num_items, 
                o_all_local, 
                o_entry_d
            )
        )

        # (4) Initialize TOTAL_AMOUNT = 0
        total_amount = 0

        # (5) Create New Order-Lines 
        ordered_items = []

        for i in range(int(num_items)):
            item_number, supplier_warehouse, quantity = data_lines[i]
            quantity = float(quantity)

            # (5a) Get S_QUANTITY 
            cur.execute(SELECT_D_NEXT_O_ID_STMT, 
                (w_id, d_id)
            )
            rows = cur.fetchone()
            s_quantity = float(rows[0])

            # (5b) Get ADJUSTED_QTY
            adjusted_qty = s_quantity - quantity

            # (5c) If ADJUSTED_QTY < 10: ADJUSTED_QTY += 100
            if adjusted_qty < 10:
                adjusted_qty += 100

            # (5d) Update the stock record 
            cur.execute(UPDATE_STOCK_QUANTITY_STMT, 
                (adjusted_qty, quantity, w_id, d_id)
            )

            if supplier_warehouse != w_id:
                cur.execute(UPDATE_STOCK_REMOTE_CNT_STMT, 
                    (w_id, d_id)
                )

            # (5e) Update ITEM_AMOUNT 
            cur.execute(SELECT_ITEM_NAME_PRICE_STMT, 
                (item_number)
            )
            rows = cur.fetchone()
            i_name, i_price = rows[0], float(rows[1])

            item_amount = quantity * i_price

            # (5f) Update TOTAL_AMOUNT 
            total_amount += item_amount

            # (5g) Create new order-line 
            ol_dist_info = "S_DIST_{}".format(d_id)
            cur.execute(INSERT_NEW_ORDER_LINE_STMT, 
                (
                    w_id, 
                    d_id, 
                    d_next_o_id, 
                    i, 
                    item_number, 
                    None, 
                    item_amount, 
                    supplier_warehouse, 
                    quantity, 
                    "S_DIST_%s".format(d_id)
                )
            )            

            ordered_items.append((
                item_number, 
                i_name, 
                supplier_warehouse, 
                quantity, 
                item_amount, 
                adjusted_qty
            ))
            
        # (6) Update TOTAL_AMOUNT 
        cur.execute(SELECT_DISTRICT_TAX_STMT, 
            (w_id, d_id)
        )
        rows = cur.fetchone()
        d_tax = float(rows[0])

        cur.execute(SELECT_WAREHOUSE_TAX_STMT, 
            (w_id)
        )
        rows = cur.fetchone()
        w_tax = float(rows[0])

        cur.execute(SELECT_CUSTOMER_DISCOUNT_STMT, 
            (w_id, d_id, c_id)
        )
        rows = cur.fetchone()
        c_discount = float(rows[0])

        total_amount = total_amount * (1.0 + d_tax + w_tax) * (1.0 - c_discount)

        cur.execute(SELECT_CUSTOMER_LAST_CREDIT_STMT, 
            (w_id, d_id, c_id)
        )
        rows = cur.fetchone()
        c_last, c_credit = rows[0], rows[1] 

        # (7) Output the following information: 
        print("1. Customer: ", w_id, d_id, c_id, c_last, c_credit, c_discount)
        print("2. Warehouse: ", w_tax, d_tax)
        print("3. Order: ", d_next_o_id, o_entry_d)
        print("4. Items: ", num_items, total_amount)
        print("5. Ordered Items: ")

        for ordered_item in ordered_items:
            print(ordered_item)

        logging.debug("new_order: status message: %s", cur.statusmessage)

    conn.commit()
    