from cassandra.cluster import Session


def execute(session: Session, *args):
    w_id, d_id, c_id =  map(int, *args[1:])

    # get customer data
    prepare_cust_data = session.prepare(
        "SELECT C_FIRST, C_MIDDLE, C_LAST, C_BALANCE FROM wholesale.Customer "
        "WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?")

    *name, c_balance = session.execute(
        prepare_cust_data.bind((w_id, d_id, c_id))).one()
    c_name = ' '.join(*name)
    print(c_name, c_balance)

    # get last order
    prepare_last_order = session.prepare(
        "SELECT O_ID, O_ENTRY_ID , O_CARRIER_ID FROM wholesale.Orders_by_cid "
        "WHERE O_W_ID = ? AND O_D_ID = ? AND O_C_ID = ? "
        "ORDER BY O_ENTRY_ID DESC LIMIT 1")

    o_id, o_entry_id, o_carrier_id = session.execute(
        prepare_last_order.bind((w_id, d_id, c_id))).one()

    print(o_id, o_entry_id, o_carrier_id)

    # get orderline data
    prepare_order_line =  session.prepare(
        "SELECT OL_I_ID, OL_SUPPLY_W_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D "
        "FROM wholesale.Orderline"
        "WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?"
    );

    items = session.execute(prepare_order_line.bind((w_id, d_id, o_id)));

    for item in items:
        print(item.OL_I_ID, item.OL_SUPPLY_W_ID,
              item.OL_QUANTITY, item.OL_AMOUNT, item.OL_DELIVERY_D)

    return



