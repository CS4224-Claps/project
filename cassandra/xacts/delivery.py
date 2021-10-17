from datetime import datetime
from cassandra.cluster import PreparedStatement, BoundStatement, Session


def execute(session: Session, args):
    w_id, carrier_id = map(int, args[1:])

    prepare_OID = session.prepare(
        "SELECT O_ID, O_CARRIER_ID FROM Orders WHERE O_W_ID = ? AND O_D_ID = ?"
    )

    prepare_update_order = session.prepare(
        "UPDATE wholesale.Orders SET O_CARRIER_ID = ? WHERE O_W_ID = ? AND O_D_ID = ? AND O_ID = ?"
    )

    prepare_update_delivery_date = session.prepare(
        "UPDATE wholesale.OrderLine SET OL_DELIVERY_D = ? WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?"
    )

    prepare_order_amount = session.prepare(
        "SELECT OL_AMOUNT FROM OrderLine WHERE O_W_ID = ? AND O_D_ID = ? AND O_ID = ?"
    )

    prepare_update_customer = session.prepare(
        "UPDATE wholesale.Customer SET C_BALANCE = C_BALANCE + ?,  C_DELIVERY_CNT = C_DELIVERY_CNT + 1"
        " WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?"
    )
    try:
        session.add_request_init_listener()
        for district in range(1, 11):
            # Get smallest OID with no carrier and Customer
            future = session.execute_async(prepare_OID.bind(w_id, district), trace=True)
            oid, cid = future.add_callback(get_smallest_oid)

            # update carrier
            session.execute(prepare_update_order.bind(carrier_id, w_id, district, oid))

            # update all order lines
            date_time = datetime.now()
            session.execute(prepare_update_delivery_date.bind(date_time, w_id, district, oid), trace=True)

            # select order amount
            future = session.execute_async(prepare_order_amount.bind(w_id, district, oid), trace=True)
            ol_total_amt = future.add_callback(get_ol_amt)

            # finally update customerrrrrr
            session.execute(prepare_update_customer.bind(ol_total_amt, w_id, district, oid), trace=True)
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
