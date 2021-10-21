def execute(session, input_arr):
    w_id, d_id, t, l = map(int, io_line)

    prepare_district = session.prepare(
        "SELECT D_NEXT_O_ID FROM District WHERE D_W_ID = ? AND D_ID = ?")
    rows = session.execute(prepare_district.bind((w_id, d_id)))
    o_id = rows[0].D_NEXT_O_ID

    prepare_order_line = session.prepare(
        "SELECT DISTINCT OL_I_ID FROM OrderLine WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID >= ? AND OL_O_ID < ?")
    rows = session.execute(prepare_order_line.bind(
        (w_id, d_id, (o_id - l), o_id)))
    i_ids = rows[0].OL_I_ID

    prepare_stock = session.prepare(
        "SELECT S_QUANTITY FROM Stock WHERE S_W_ID = ? AND S_I_ID = ?")
    cnt = 0
    for i_id in i_ids:
        rows = session.execute(prepare_stock.bind((w_id, i_id)))
        if rows and rows[0].S_QUANTITY < t:
            cnt = cnt + 1

    return count
