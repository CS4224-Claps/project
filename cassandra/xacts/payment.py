from decimal import Decimal


def execute(session, input_arr):
    _, w_id, d_id, c_id, pay_amt = input_arr
    w_id, d_id, c_id, pay_amt = int(w_id), int(
        d_id), int(c_id), Decimal(pay_amt)

    # Update warehouse
    prepare_warehouse = session.prepare(
        "SELECT W_YTD, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP FROM Warehouse WHERE W_ID = ?")
    rows = session.execute(prepare_warehouse.bind((w_id)))
    warehouse = rows[0]
    w_addr = warehouse[1:]
    updated_w_ytd = warehouse.W_YTD + pay_amt

    prepare_update_warehouse = session.prepare(
        "UPDATE Warehouse SET W_YTD = ? WHERE W_ID = ?")
    session.execute(prepare_update_warehouse.bind((updated_w_ytd, w_id)))

    # Update district
    prepare_district = session.prepare(
        "SELECT D_YTD, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP FROM District WHERE D_W_ID = ? AND D_ID = ?")
    rows = session.execute(prepare_district.bind((w_id, d_id)))
    district = rows[0]
    d_addr = rows[1:]
    updated_d_ytd = district.D_YTD + pay_amt

    prepare_update_district = session.prepare(
        "UPDATE District SET D_YTD = ? WHERE D_W_ID = ? AND D_ID = ?")
    session.execute(prepare_update_district.bind((updated_d_ytd, w_id, d_id)))

    # Update customer
    prepare_customer = session.prepare(
        "SELECT * FROM  Customer WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?")
    rows = session.execute(prepare_customer.bind((w_id, d_id, c_id)))
    customer = rows[0]
    cust = customer[:17]
    c_balance, c_ytd_payment, c_payment_cnt = customer.C_BALANCE, customer.C_YTD_PAYMENT, customer.C_PAYMENT_CNT
    c_balance -= pay_amt
    c_ytd_payment += pay_amt
    c_payment_cnt += 1

    prepare_update_customer = session.prepare(
        "UPDATE Customer SET C_BALANCE = ?, C_YTD_PAYMENT = ?, C_PAYMENT_CNT = ? WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?")
    session.execute(prepare_update_customer.bind(
        (c_balance, c_ytd_payment, c_payment_cnt, w_id, d_id, c_id)))

    print("1. Customer info: ", cust)
    print("2. Warehouse address : ", w_addr)
    print("3. District address: ", d_addr)
    print("4. Payment amount: ", pay_amt)
