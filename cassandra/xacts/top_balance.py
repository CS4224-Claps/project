from utils.decorators import log_command


@log_command
def execute(session, args):
    # Get top 10 customers per partition
    customers = [
        customer
        for customer in session.execute(
            "SELECT C_FIRST, C_MIDDLE, C_LAST, C_BALANCE, W_NAME, D_NAME FROM wholesale.Customer_by_balance PER PARTITION LIMIT 10"
        )
    ]

    # Sort customers across all partitions to get top 10 balances globally
    customers.sort(key=lambda customer: customer.c_balance, reverse=True)

    # Print info
    print("Customers:")
    for customer in customers[:10]:
        print(
            f"{customer.c_first} {customer.c_middle} {customer.c_last} {customer.c_balance} {customer.w_name} {customer.d_name}"
        )
