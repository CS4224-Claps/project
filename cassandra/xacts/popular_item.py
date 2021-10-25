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
    orders = []
    for o_id in range(d_next_o_id - num_orders, d_next_o_id):
        prepare_order = session.prepare(
            "SELECT O_ID, O_ENTRY_D, O_C_ID FROM wholesale.Orders WHERE O_W_ID = ? AND O_D_ID = ? AND  O_ID = ?"
        )
        rows = session.execute(prepare_order.bind((w_id, d_id, o_id)))
        order = rows[0]
        orders.append(order)

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
    order_popular_items = []
    # Maintain an overall map of popular item id : id names
    popular_item_id_names = {}
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
        order_popular_items.append(popular_items)
        popular_item_id_names[row.ol_i_id] = row.i_name

    # Calculate the number of orders that contain each popular item
    popular_item_occurrences = {i_id: 0 for i_id in popular_item_id_names}
    for i_id in popular_item_occurrences:
        for order_item_set in order_item_sets:
            if i_id in order_item_set:
                popular_item_occurrences[i_id] += 1

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
        for item in order_popular_items[i]:
            print("  ", item.i_name, item.ol_quantity)

    print(f"4. Percentage of popular items in last {num_orders} orders: ")
    for item_id, occurrences in popular_item_occurrences.items():
        print(
            "  ", popular_item_id_names[item_id], f"{occurrences / num_orders * 100}%"
        )
