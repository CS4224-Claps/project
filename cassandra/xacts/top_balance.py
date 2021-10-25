from utils.decorators import log_command


@log_command
def execute(session, args):
    # Get top 10 customers
    customers = [
        customer
        for customer in session.execute(
            "SELECT C_FIRST, C_MIDDLE, C_LAST, C_BALANCE, W_NAME, D_NAME FROM wholesale.Customer_by_balance LIMIT 10"
        )
    ]

    # Print info
    print("Customers:")
    for customer in customers:
        print(
            f"{customer.c_first} {customer.c_middle} {customer.c_last} {customer.c_balance} {customer.w_name} {customer.d_name}"
        )
