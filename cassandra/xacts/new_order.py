from datetime import datetime, timezone
from decimal import Decimal


def execute(session, input_arr, data_lines=[]):
    c_id, w_id, d_id, num_items = map(int, input_arr[1:])

    # Get D_NEXT_O_ID, D_TAX and W_TAX
    prepare_district = session.prepare(
        "SELECT D_NEXT_O_ID, D_TAX, W_TAX FROM District WHERE D_W_ID = ? AND D_ID = ?")
    rows = session.execute(prepareDistrict.bind((w_id, d_id)))
    district = rows[0]
    o_id, d_tax, w_tax = int(district.D_NEXT_O_ID), Decimal(
        district.D_TAX), Decimal(district.W_TAX)

    # Update D_NEXT_O_OID by 1
    prepare_update_district = session.prepare(
        "UPDATE District SET D_NEXT_O_ID = ? WHERE D_W_ID = ? AND D_ID = ?")
    session.execute(prepare_update_district.bind(
        ((o_id + 1), w_id, d_id)))

    # Create new order
    o_all_local = 1
    for i in range(int(num_items)):
        _, supplier_warehouse, _ = data_lines[i]
        if supplier_warehouse != w_id:
            o_all_local = 0
            break

    o_entry_d = datetime.now(timezone.utc)

    prepare_create_order = session.prepare(
        "INSERT INTO Orders (O_W_ID, O_D_ID, O_ID, O_C_ID, O_CARRIER_ID, O_OLCNT, O_ALL_LOCAL, O_ENTRY_D) VALUES (?,?,?,?,?,?,?,?)")
    session.execute(prepare_create_order.bind(w_id, d_id, o_id,
                                              c_id, None, num_items, o_all_local, o_entry_d))

    # Initialize total amt
    total_amount = 0

    # Create new order lines
    ordered_items_pretty = []

    for i in range(int(num_items)):
        item_number, supplier_warehouse, quantity = (
            int(data_lines[i][0]),
            int(data_lines[i][1]),
            Decimal(data_lines[i][2]),
        )

        # Get s_qty, s_ytd, s_order_cnt, s_remote_cnt, i_name and i_qny
        prepare_stock = session.prepare(
            "SELECT S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT, I_NAME, I_PRICE FROM Stock WHERE S_W_ID = ? AND S_I_ID = ?")
        rows = session.execute(prepare_stock.bind(
            (supplier_warehouse, item_number)))
        stock = rows[0]

        s_quantity, s_ytd, s_order_cnt, s_remote_cnt, i_name, i_price = Decimal(stock.S_QUANTITY), Decimal(
            stock.S_YTD), int(stock.S_ORDER_CNT), int(S_REMOTE_CNT), stock.I_NAME, Decimal(stock.I_PRICE)

        adjusted_qty = s_quantity - quantity
        if adjusted_qty < 10:
            adjusted_qty += 100
        adjusted_remote_cnt = s_remote_cnt + \
            1 if supplier_warehouse != w_id else s_remote_cnt

        # Update stock table
        prepare_update_stock = session.prepare(
            "UPDATE Stock SET S_QUANTITY = ?, S_YTD = ?, S_ORDER_CNT = ?, S_REMOTE_CNT = ?")
        session.execute(prepare_update_stock.bind((adjusted_qty, s_ytd + quantity,
                                                   s_order_cnt + 1, adjusted_remote_cnt, supplier_warehouse, item_number)))

        # update item amt and total amt
        item_amount = quantity * i_price
        total_amount += item_amount

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

        # create new orderlines
        prepare_insert_order_line = session.prepare(
            "INSERT INTO OrderLine (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER, OL_I_ID, OL_DELIVERY_D, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO) VALUES (?,?,?,?,?,?,?,?,?,?)")
        session.execute(prepare_insert_order_line.bind((w_id, d_id, o_id, i, item_number,
                                                        None, item_amount, supplier_warehouse, quantity, "S_DIST_{:02d}".format(int(d_id)))))
    prepare_customer = session.prepare(
        "SELECT C_LAST, C_CREDIT, C_DISCOUNT FROM Customer WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?")
    rows = session.execute(prepare_customer.bind((w_id, d_id, c_id)))
    customer = rows[0]
    c_last, c_credit, c_discount = customer.C_LAST, customer.C_CREDIT, Decimal(
        customer.C_DISCOUNT)

    total_amount = total_amount * \
        (1 + d_tax + w_tax) * (1 - c_discount)

    print("1. Customer: ", w_id, d_id, c_id, c_last,
          c_credit, c_discount)
    print("2. Warehouse: ", w_tax, "District: ", d_tax)
    print("3. Order: ", o_id, o_entry_d)
    print("4. Items: ", num_items, round(total_amount, 2))
    print("5. Ordered Items: ")

    for ordered_item in ordered_items_pretty:
        print(ordered_item)
