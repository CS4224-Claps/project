from datetime import datetime
from cassandra.cluster import PreparedStatement, BoundStatement, Session


def execute(session: Session, args):
    w_id, carrier_id = map(int, args[1:])

    prepare_OID = session.prepare(
        "SELECT O_ID, O_CARRIER_ID, O_C_ID FROM Orders WHERE O_W_ID = ? AND O_D_ID = ?"
    )

    prepare_update_order = session.prepare(
        "UPDATE wholesale.Orders SET O_CARRIER_ID = ? WHERE O_W_ID = ? AND O_D_ID = ? AND O_ID = ?"
    )
    
    prepare_ol_num = session.prepare(
        "SELECT OL_NUMBER, OL_AMOUNT FROM wholesale.Orderline WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?"
    )

    prepare_orderline_data = session.prepare(
        "SELECT OL_AMOUNT, OL_NUMBER FROM OrderLine WHERE O_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?"
    )

    prepare_update_delivery_date = session.prepare(
        "UPDATE wholesale.OrderLine SET OL_DELIVERY_D = ? WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ? AND OL_NUMBER = ?"
    )

    prepare_cust_data = session.prepare(
        "SELECT C_BALANCE, C_DELIVERY_CNT FROM wholesale.Customer WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?"
    )


    prepare_update_customer = session.prepare(
        "UPDATE wholesale.Customer SET C_BALANCE = ?,  C_DELIVERY_CNT = ? WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?"
    )

    try:
        #session.add_request_init_listener()
        for district in range(1, 11):
            # Get smallest OID with no carrier and Customer
            future = session.execute_async(prepare_OID.bind(w_id, district), trace=True)
            oid, carrier_id, c_id = future.add_callback(get_smallest_oid)

            # update carrier
            session.execute(prepare_update_order.bind(carrier_id, w_id, district, oid), trace=True)

            # prepare order line data
            ol_rows = session.execute(prepare_orderline_data.bind(w_id, district, oid), trace=True)
            c_balance_add = get_ol_amt(ol_rows)
            c_delivery_add = 1

            # update all order lines
            date_time = datetime.now()
            for ol_row in ol_rows:
                session.execute(prepare_update_delivery_date.bind(date_time, w_id, district, oid, ol_row.OL_NUMBER),
                                trace=True)

            # prepare customer data
            c_balance, c_delivery = session.execute(prepare_cust_data.bind(w_id, district, c_id))
            c_balance += c_balance_add
            c_delivery += 1

            # finally update customerrrrrr
            session.execute(prepare_update_customer.bind(c_balance, c_delivery, w_id, district, c_id), trace=True)
    except TimeoutError as e:
        print("add try again")


def get_smallest_oid(rows):
    for row in rows:
        if not row.O_CARRIER.ID:
            return int(row.O_ID), int(row.O_C_ID)


def get_ol_amt(rows):
    total = 0
    for row in rows:
        total += row.OL_AMOUNT

    return total
