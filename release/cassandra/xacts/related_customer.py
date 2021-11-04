from utils.decorators import log_command


@log_command
def execute(session, args):
    c_w_id, c_d_id, c_id = map(int, args[1:])

    # Get o_ids of all the customer's orders
    prepare_orders = session.prepare(
        "SELECT O_ID FROM wholesale.Orders WHERE O_W_ID = ? AND O_D_ID = ? AND O_C_ID = ? ALLOW FILTERING"
    )
    rows = session.execute(prepare_orders.bind((c_w_id, c_d_id, c_id)))
    o_ids = [order.o_id for order in rows]

    # Get items for each order
    order_itemsets = []
    prepare_orderline = session.prepare(
        "SELECT OL_I_ID FROM wholesale.Orderline WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?"
    )
    for o_id in o_ids:
        rows = session.execute(prepare_orderline.bind((c_w_id, c_d_id, o_id)))
        order_itemsets.append({orderline.ol_i_id for orderline in rows})

    # For each of customer's orders, find all orders from different warehouse with >=2 common items
    related_orders = set()
    prepare_orderline = session.prepare(
        "SELECT * FROM wholesale.Orderline_by_iid WHERE OL_I_ID IN ?"
    )
    for order_itemset in order_itemsets:
        seen_order_identifiers = set()
        rows = session.execute(prepare_orderline.bind((order_itemset,)))
        for row in rows:
            # Related customer must be from different warehouse
            if row.ol_w_id == c_w_id:
                continue
            # order_identifier is (w_id, d_id, o_id)
            order_identifier = (row.ol_w_id, row.ol_d_id, row.ol_o_id)
            if order_identifier in seen_order_identifiers:
                # This is the second time we see the same order identifier - it is a related customer
                related_orders.add(order_identifier)
            seen_order_identifiers.add(order_identifier)

    # Retrieve c_id for these related customers' orders
    prepare_orders = session.prepare(
        "SELECT O_C_ID FROM wholesale.Orders WHERE O_W_ID = ? AND O_D_ID = ? AND O_ID = ?"
    )
    related_customers = []
    for w_id, d_id, o_id in related_orders:
        rows = session.execute(prepare_orders.bind((w_id, d_id, o_id)))
        related_c_id = rows[0].o_c_id
        related_customers.append((w_id, d_id, related_c_id))

    print("1. Customer: ", c_w_id, c_d_id, c_id)
    print("2. Related customers: ")
    for customer in related_customers:
        print(*customer)
