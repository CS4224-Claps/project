from datetime import datetime
from cassandra.cluster import PreparedStatement, BoundStatement, Session
from utils.decorators import log_command


@log_command
def execute(session: Session, args):
    w_id, carrier_id = map(int, args[1:])

    prepare_OID = session.prepare(
        "SELECT O_ID, O_CARRIER_ID, O_C_ID FROM wholesale.Orders WHERE O_W_ID = ? AND O_D_ID = ? ORDER BY O_ID ASC"
    )

    prepare_update_order = session.prepare(
        "UPDATE wholesale.Orders SET O_CARRIER_ID = ? WHERE O_W_ID = ? AND O_D_ID = ? AND O_ID = ?"
    )

    prepare_orderline_data = session.prepare(
        "SELECT OL_AMOUNT, OL_NUMBER FROM wholesale.OrderLine WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?"
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
        print("new transaction")
        # session.add_request_init_listener()
        for district in range(1, 11):
            # Get smallest OID with no carrier and Customer
            oid_rows = session.execute(prepare_OID.bind((w_id, district)), trace=True)
            res = get_smallest_oid(oid_rows)

            if res is None:
                continue

            oid, c_id = res

            # update carrier
            session.execute(
                prepare_update_order.bind((carrier_id, w_id, district, oid)), trace=True
            )

            # prepare order line data
            ol_rows = session.execute(
                prepare_orderline_data.bind((w_id, district, oid)), trace=True
            )
            c_balance_add = get_ol_amt(ol_rows)

            # update all order lines
            date_time = datetime.now()
            for ol_row in ol_rows:
                session.execute(
                    prepare_update_delivery_date.bind(
                        (date_time, w_id, district, oid, ol_row.OL_NUMBER)
                    ),
                    trace=True,
                )

            # prepare customer data
            c_row = session.execute(
                prepare_cust_data.bind((w_id, district, c_id))
            ).one()
            c_balance = c_row.c_balance + c_balance_add
            c_delivery = c_row.c_delivery_cnt + 1

            # finally update customerrrrrr
            session.execute(
                prepare_update_customer.bind(
                    (c_balance, c_delivery, w_id, district, c_id)
                ),
                trace=True,
            )

    except TimeoutError as e:
        print("add try again")


def get_smallest_oid(rows):
    for row in rows:
        if not row.o_carrier_id:
            return int(row.o_id), int(row.o_c_id)


def get_ol_amt(rows):
    total = 0
    for row in rows:
        total += row.ol_amount

    return total
