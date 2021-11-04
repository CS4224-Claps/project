from utils.decorators import log_command


@log_command
def execute(session, args):
    w_id, d_id, num_orders = map(int, args[1:])

    # Get D_NEXT_O_ID
    prepare_district = session.prepare(
        "SELECT D_NEXT_O_ID FROM wholesale.District WHERE D_W_ID = ? AND D_ID = ?"
    )
    rows = session.execute(prepare_district.bind((w_id, d_id)))
    district = rows[0]
    d_next_o_id = int(district.d_next_o_id)

    # Get last L orders
    prepare_order = session.prepare(
        "SELECT O_ID, O_ENTRY_D, O_C_ID FROM wholesale.Orders WHERE O_W_ID = ? AND O_D_ID = ? AND  O_ID >= ?"
    )
    rows = session.execute(prepare_order.bind((w_id, d_id, d_next_o_id - num_orders)))
    orders = [order for order in rows]

    # Get customer info for last L orders
    customers = []
    for order in orders:
        prepare_customer = session.prepare(
            "SELECT C_FIRST, C_MIDDLE, C_LAST FROM wholesale.Customer WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?"
        )
        rows = session.execute(prepare_customer.bind((w_id, d_id, order.o_c_id)))
        customer = rows[0]
        customers.append(customer)

    # Examine order lines for last L orders
    # Maintain a set of I_IDs for all items for each order (to check for presence of popular item)
    order_item_sets = []
    # Maintain a list of popular items for each order
    order_popular_item_lists = []
    for order in orders:
        prepare_orderline = session.prepare(
            "SELECT OL_I_ID, I_NAME, OL_QUANTITY FROM wholesale.OrderLine WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?"
        )
        rows = session.execute(prepare_orderline.bind((w_id, d_id, order.o_id)))
        order_item_set = set()
        max_qty = 0
        popular_items = []
        for row in rows:
            order_item_set.add(row.ol_i_id)
            if row.ol_quantity == max_qty:
                popular_items.append(row)
            elif row.ol_quantity > max_qty:
                max_qty = row.ol_quantity
                popular_items = [row]
        order_item_sets.append(order_item_set)
        order_popular_item_lists.append(popular_items)

    # Count the number of popular item occurrences {(id, name): int}
    popular_item_occurrences = {}
    for order_popular_item_list in order_popular_item_lists:
        for popular_item in order_popular_item_list:
            popular_item_occurrences[(popular_item.ol_i_id, popular_item.i_name)] = 0

    for i_id, i_name in popular_item_occurrences.keys():
        for order_item_set in order_item_sets:
            if i_id in order_item_set:
                popular_item_occurrences[(i_id, i_name)] += 1

    # Print info
    print("1. District: ", w_id, d_id)
    print("2. Number of last orders: ", num_orders)
    print("3. For each order: ")
    for i, order in enumerate(orders):
        print("Order: ", order.o_id, order.o_entry_d)
        print(
            "Customer: ",
            customers[i].c_first,
            customers[i].c_middle,
            customers[i].c_last,
        )
        print("Popular items: ")
        for item in order_popular_item_lists[i]:
            print("  ", item.i_name, item.ol_quantity)

    print(f"4. Percentage of popular items in last {num_orders} orders: ")
    for (_, i_name), occurrences in popular_item_occurrences.items():
        print(
            "  ", i_name, f"{occurrences / num_orders * 100}%"
        )
