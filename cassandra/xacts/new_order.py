from datetime import datetime, timezone
from utils.decorators import log_command


@log_command
def execute(session, input_arr, data_lines=[]):
    c_id, w_id, d_id, num_items = map(int, input_arr[1:])

    # Get D_NEXT_O_ID (1), D_TAX (6) and W_TAX (6)
    prepare_district = session.prepare(
        "SELECT D_NEXT_O_ID, D_TAX, W_TAX FROM wholesale.District WHERE D_W_ID = ? AND D_ID = ?"
    )
    d_rows = session.execute(prepare_district.bind((w_id, d_id)))

    if not d_rows:
        return None

    district = d_rows[0]
    o_id, d_tax, w_tax = (
        int(district.d_next_o_id),
        float(district.d_tax),
        float(district.w_tax),
    )

    # Update D_NEXT_O_OID by 1 (2)
    prepare_update_district = session.prepare(
        "UPDATE wholesale.District SET D_NEXT_O_ID = ? WHERE D_W_ID = ? AND D_ID = ?"
    )
    session.execute(prepare_update_district.bind(((o_id + 1), w_id, d_id)))

    # Create new order (3)
    o_all_local = 1
    for i in range(int(num_items)):
        _, supplier_warehouse, _ = data_lines[i]
        if supplier_warehouse != w_id:
            o_all_local = 0
            break

    o_entry_d = datetime.now(timezone.utc)

    prepare_create_order = session.prepare(
        "INSERT INTO wholesale.Orders (O_W_ID, O_D_ID, O_ID, O_C_ID, O_CARRIER_ID, \
        O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D) VALUES (?,?,?,?,?,?,?,?)"
    )
    session.execute(
        prepare_create_order.bind(
            (w_id, d_id, o_id, c_id, None, num_items, o_all_local, o_entry_d)
        )
    )

    # Initialize total amt (4)
    total_amount = 0
    ordered_items_pretty = []

    # (5)
    for i in range(int(num_items)):
        item_number, supplier_warehouse, quantity = (
            int(data_lines[i][0]),
            int(data_lines[i][1]),
            float(data_lines[i][2]),
        )

        # Get s_qty, s_ytd, s_order_cnt, s_remote_cnt, i_name and i_qnty
        prepare_stock = session.prepare(
            "SELECT S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT, I_NAME, I_PRICE \
            FROM wholesale.Stock WHERE S_W_ID = ? AND S_I_ID = ?"
        )
        s_rows = session.execute(prepare_stock.bind((supplier_warehouse, item_number)))

        if not s_rows:
            return None

        stock = s_rows[0]
        s_quantity, s_ytd, s_order_cnt, s_remote_cnt, i_name, i_price = (
            float(stock.s_quantity),
            float(stock.s_ytd),
            int(stock.s_order_cnt),
            int(stock.s_remote_cnt),
            stock.i_name,
            float(stock.i_price),
        )

        # (5c)
        adjusted_qty = s_quantity - quantity
        if adjusted_qty < 10:
            adjusted_qty += 100
        adjusted_remote_cnt = (
            s_remote_cnt + 1 if supplier_warehouse != w_id else s_remote_cnt
        )

        # Update stock table (5d)
        prepare_update_stock = session.prepare(
            "UPDATE wholesale.Stock SET S_QUANTITY = ?, S_YTD = ?, S_ORDER_CNT = ?, S_REMOTE_CNT = ? \
            WHERE S_W_ID = ? AND S_I_ID = ?"
        )
        session.execute(
            prepare_update_stock.bind(
                (
                    adjusted_qty,
                    s_ytd + quantity,
                    s_order_cnt + 1,
                    adjusted_remote_cnt,
                    supplier_warehouse,
                    item_number,
                )
            )
        )

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

        # create new orderline (5g)
        prepare_insert_order_line = session.prepare(
            "INSERT INTO wholesale.OrderLine (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER, \
            OL_I_ID, OL_DELIVERY_D, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO) \
            VALUES (?,?,?,?,?,?,?,?,?,?)"
        )
        session.execute(
            prepare_insert_order_line.bind(
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
        )

    prepare_customer = session.prepare(
        "SELECT C_LAST, C_CREDIT, C_DISCOUNT FROM wholesale.Customer \
        WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?"
    )
    c_rows = session.execute(prepare_customer.bind((w_id, d_id, c_id)))

    if not c_rows:
        return None

    customer = c_rows[0]
    c_last, c_credit, c_discount = (
        customer.c_last,
        customer.c_credit,
        float(customer.c_discount),
    )

    total_amount = total_amount * (1 + d_tax + w_tax) * (1 - c_discount)

    print("1. Customer: ", w_id, d_id, c_id, c_last, c_credit, c_discount)
    print("2. Warehouse: ", w_tax, "District: ", d_tax)
    print("3. Order: ", o_id, o_entry_d)
    print("4. Items: ", num_items, round(total_amount, 2))
    print("5. Ordered Items: ")
    for ordered_item in ordered_items_pretty:
        print(ordered_item)
