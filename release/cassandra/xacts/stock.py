from utils.decorators import log_command


@log_command
def execute(session, input_arr):
    w_id, d_id, t, l = map(int, input_arr[1:])

    prepare_district = session.prepare(
        "SELECT D_NEXT_O_ID FROM wholesale.District WHERE D_W_ID = ? AND D_ID = ?"
    )
    d_rows = session.execute(prepare_district.bind((w_id, d_id)))

    if not d_rows:
        return None

    o_id = int(d_rows[0].d_next_o_id)

    prepare_order_line = session.prepare(
        "SELECT OL_I_ID FROM wholesale.OrderLine \
        WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID >= ? AND OL_O_ID < ?"
    )
    ol_rows = session.execute(prepare_order_line.bind((w_id, d_id, (o_id - l), o_id)))

    prepare_stock = session.prepare(
        "SELECT S_QUANTITY FROM wholesale.Stock WHERE S_W_ID = ? AND S_I_ID = ?"
    )
    cnt = 0

    # remove dulpicates
    i_ids = set([ol_row.ol_i_id for ol_row in ol_rows])

    for i_id in i_ids:
        s_rows = session.execute(prepare_stock.bind((w_id, i_id)))

        if s_rows and s_rows[0].s_quantity < t:
            cnt += 1

    print("Total Number of Items: ", cnt)
