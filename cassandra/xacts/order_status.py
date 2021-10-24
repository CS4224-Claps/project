from cassandra.cluster import Session
from utils.decorators import log_command


@log_command
def execute(session: Session, args):
    w_id, d_id, c_id =  map(int, args[1:])

    # get customer data
    prepare_cust_data = session.prepare(
        "SELECT C_FIRST, C_MIDDLE, C_LAST, C_BALANCE FROM wholesale.Customer "
        "WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?")

    c_first, c_middle, c_last, c_balance = session.execute(
        prepare_cust_data.bind((w_id, d_id, c_id))).one()
    c_name = c_first + c_middle + c_last
    print(c_name, c_balance)

    # get last order
    prepare_last_order = session.prepare(
        "SELECT O_ID, O_ENTRY_D , O_CARRIER_ID FROM wholesale.Orders_by_cid "
        "WHERE O_W_ID = ? AND O_D_ID = ? AND O_C_ID =?")

    orders = session.execute(
        prepare_last_order.bind((w_id, d_id, c_id)))

    o_id, o_entry_d, o_carrier_id = get_order_data(orders)

    print(o_id, o_entry_d, o_carrier_id)

    # get orderline data
    prepare_order_line = session.prepare(
        "SELECT OL_I_ID, OL_SUPPLY_W_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D FROM wholesale.Orderline "
        "WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID = ?")

    result = session.execute(prepare_order_line.bind((w_id, d_id, o_id)), trace=True)
    items = result.result()
    tracing = result.get_query_trace()

    for e in tracing.events:
        logging.debug(e)

    for item in items:
        print(item.ol_i_id, item.ol_supply_w_id,
              item.ol_quantity, item.ol_amount, item.ol_delivery_d)
    return

def get_order_data(orders):
    result_id, result_entry_d, result_carrier_id = None, None, None
    for order in orders:
        if (not result_entry_d) or order.o_entry_d > result_entry_d:
            result_id= order.o_id
            result_entry_d = order.o_entry_d
            result_carrier_id = order.o_carrier_id
    return result_id, result_entry_d, result_carrier_id
              

