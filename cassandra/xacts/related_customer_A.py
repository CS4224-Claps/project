from collections import defaultdict

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

    # Get orderlines
    order_itemmap = defaultdict(set)
    rows = session.execute("SELECT OL_W_ID, OL_D_ID, OL_O_ID, OL_I_ID FROM Orderline ALLOW FILTERING")
    for row in rows:
        order_itemmap[(row.ol_w_id, row.ol_d_id, row.ol_o_id)].add(row.ol_i_id)

    # For each of customer's orders, find all orders from different warehouse with >=2 common items
    related_customers = set()
    for order_itemset in order_itemsets:
        for order_identifier, other_order_itemset in order_itemmap.items():
            if order_identifier[0] == c_w_id:
                continue
            if len(order_itemset.intersection(other_order_itemset)) >= 2:
                related_customers.add(order_identifier)

    # Retrieve c_id for these related customers' orders
    print("1. Customer: ", c_w_id, c_d_id, c_id)
    print("2. Related customers: ")
    for customer in related_customers:
        print(*customer)
