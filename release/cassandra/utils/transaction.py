from xacts import (
    new_order,
    payment,
    delivery,
    order_status,
    stock,
    popular_item,
    top_balance,
    related_customer,
)

command_to_func = {
    "N": new_order,
    "P": payment,
    "D": delivery,
    "O": order_status,
    "S": stock,
    "I": popular_item,
    "T": top_balance,
    "R": related_customer,
}


def run_xact(xact_type, session, *args):
    if xact_type in command_to_func:
        xact = command_to_func.get(xact_type)
        return xact.execute(session, *args)
