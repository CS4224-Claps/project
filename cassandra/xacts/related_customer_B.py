def execute(session, input_arr, data_lines=[]):
    c_w_id, c_d_id, c_id = map(int, input_arr[1:])

    # Get o_ids of all the customer's orders
    prepare_orders = session.prepare(
        "SELECT O_ID FROM Orders WHERE O_W_ID = ? AND O_D_ID = ? AND O_C_ID = ? ALLOW FILTERING")
    rows = session.execute(prepare_orders.bind((c_w_id, c_d_id, c_id)))
    o_ids = [order.o_id for order in rows]

    # Get items for each order
    order_itemsets = []
    prepare_orderline = session.prepare(
        "SELECT OL_I_ID FROM Orderline WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?")
    for o_id in o_ids:
        rows = session.execute(prepare_orderline.bind((c_w_id, c_d_id, o_id)))
        order_itemsets.append({orderline.ol_i_id for orderline in rows})
        
    # For each order, retrieve ordersets for all the items that are in it
    # If an order identifer appears twice among these ordersets, and the w_id is different, this is a related customer
    related_customers = set()
    prepare_item = session.prepare(
        "SELECT ORDER_SET FROM Item WHERE I_ID IN ?")
    for order_itemset in order_itemsets:
        seen_order_identifiers = set()
        rows = session.execute(prepare_item.bind((order_itemset,)))
        for row in rows:
            order_set = row.order_set
            for order_identifier in order_set:
                # order_identifier is (w_id, d_id, o_id, c_id)
                if order_identifier[0] == c_w_id:
                    # Related customer must be from a different warehouse
                    continue
                if order_identifier in seen_order_identifiers:
                    # This is the second time we see the same order identifier - it is a related customer
                    related_customers.add((order_identifier[0], order_identifier[1], order_identifier[3]))
                seen_order_identifiers.add(order_identifier)
    print("1. Customer: ", c_w_id, c_d_id, c_id)
    print("2. Related customers: ")
    for customer in related_customers:
        print(*customer)
