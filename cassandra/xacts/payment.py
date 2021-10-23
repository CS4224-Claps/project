def execute(session, input_arr):
    _, w_id, d_id, c_id, pay_amt = input_arr
    w_id, d_id, c_id, pay_amt = int(w_id), int(
        d_id), int(c_id), float(pay_amt)

    # Update warehouse
    prepare_warehouse = session.prepare(
        "SELECT W_YTD, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP \
        FROM wholesale.Warehouse WHERE W_ID = ?")
    w_rows = session.execute(prepare_warehouse.bind([w_id]))

    if not w_rows:
        return None

    warehouse = w_rows[0]
    updated_w_ytd = float(warehouse.w_ytd) + pay_amt

    prepare_update_warehouse = session.prepare(
        "UPDATE wholesale.Warehouse SET W_YTD = ? WHERE W_ID = ?")
    session.execute(prepare_update_warehouse.bind((updated_w_ytd, w_id)))

    # Update district
    prepare_district = session.prepare(
        "SELECT D_YTD, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP \
        FROM wholesale.District WHERE D_W_ID = ? AND D_ID = ?")
    d_rows = session.execute(prepare_district.bind((w_id, d_id)))

    if not d_rows:
        return None

    district = d_rows[0]
    updated_d_ytd = float(district.d_ytd) + pay_amt

    prepare_update_district = session.prepare(
        "UPDATE wholesale.District SET D_YTD = ? WHERE D_W_ID = ? AND D_ID = ?")
    session.execute(prepare_update_district.bind((updated_d_ytd, w_id, d_id)))

    # Update customer
    prepare_customer = session.prepare(
        "SELECT C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, \
        C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT \
        FROM wholesale.Customer WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?")
    c_rows = session.execute(prepare_customer.bind((w_id, d_id, c_id)))

    if not c_rows:
        return None

    customer = c_rows[0]
    c_balance, c_ytd_payment, c_payment_cnt = float(customer.c_balance), float(
        customer.c_ytd_payment), int(customer.c_payment_cnt)
    c_balance -= pay_amt
    c_ytd_payment += pay_amt
    c_payment_cnt += 1

    prepare_update_customer = session.prepare(
        "UPDATE wholesale.Customer SET C_BALANCE = ?, C_YTD_PAYMENT = ?, C_PAYMENT_CNT = ? \
        WHERE C_W_ID = ? AND C_D_ID = ? AND C_ID = ?")
    session.execute(prepare_update_customer.bind(
        (c_balance, c_ytd_payment, c_payment_cnt, w_id, d_id, c_id)))

    # use c_balance as it is updated
    print("1. Customer info:", w_id, d_id, c_id, *customer[:-3], c_balance)
    print("2. Warehouse address : ", *warehouse[1:])
    print("3. District address: ", *district[1:])
    print("4. Payment amount: ", pay_amt)
