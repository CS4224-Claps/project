warehouse_read_headers = [
    'w_id',
    'w_name',
    'w_street_1',
    'w_street_2',
    'w_city',
    'w_state',
    'w_zip',
    'w_tax',
]

warehouse_write_headers = [
    'w_id',
    'w_ytd',
]

district_read_headers = [
    'd_w_id',
    'd_id',
    'd_name',
    'd_street_1',
    'd_street_2',
    'd_city',
    'd_state',
    'd_zip',
    'd_tax',
]

district_write_headers = [
    'd_w_id',
    'd_id',
    'd_ytd',
    'd_next_o_id',
]

customer_read_headers = [
    'c_w_id',
    'c_d_id',
    'c_id',
    'c_first',
    'c_middle',
    'c_last',
    'c_street_1',
    'c_street_2',
    'c_city',
    'c_state',
    'c_zip',
    'c_phone',
    'c_since',
    'c_credit',
    'c_credit_lim',
    'c_discount',
]

customer_write_headers = [
    'c_w_id',
    'c_d_id',
    'c_id',
    'c_balance',
    'c_ytd_payment',
    'c_payment_cnt',
    'c_delivery_cnt',
]

customer_misc_headers = [
    'c_w_id',
    'c_d_id',
    'c_id',
    'c_data',
]

order_read_headers = [
    'o_w_id',
    'o_d_id',
    'o_id',
    'o_c_id',
    'o_ol_cnt',
    'o_all_local',
    'o_entry_d',
]

order_write_headers = [
    'o_w_id',
    'o_d_id',
    'o_id',
    'o_c_id',
    'o_carrier_id',
]

item_read_headers = [
    'i_id',
    'i_name',
    'i_price',
]

item_misc_headers = [
    'i_id',
    'i_name',
    'i_im_id',
    'i_data',
]

order_line_read_headers = [
    'ol_w_id',
    'ol_d_id',
    'ol_o_id',
    'ol_number',
    'ol_i_id',
    'ol_amount',
    'ol_supply_w_id',
    'ol_quantity',
    'ol_dist_info',
]

order_line_write_headers = [
    'ol_w_id',
    'ol_d_id',
    'ol_o_id',
    'ol_number',
    'ol_i_id',
    'ol_delivery_d',
]

stock_write_headers = [
    's_w_id',
    's_i_id',
    's_quantity',
    's_ytd',
    's_order_cnt',
    's_remote_cnt',
]

stock_misc_headers = [
    's_w_id',
    's_i_id',
    's_dist_01',
    's_dist_02',
    's_dist_03',
    's_dist_04',
    's_dist_05',
    's_dist_06',
    's_dist_07',
    's_dist_08',
    's_dist_09',
    's_dist_10',
    's_data',
]

dist_header_mappings = {
    'warehouse_read_headers': warehouse_read_headers, 
    'warehouse_write_headers': warehouse_write_headers, 
    'district_read_headers': district_read_headers, 
    'district_write_headers': district_write_headers, 
    'customer_read_headers': customer_read_headers, 
    'customer_write_headers': customer_write_headers, 
    'customer_misc_headers': customer_misc_headers, 
    'order_read_headers': order_read_headers, 
    'order_write_headers': order_write_headers, 
    'item_read_headers': item_read_headers, 
    'item_misc_headers': item_misc_headers, 
    'order_line_read_headers': order_line_read_headers, 
    'order_line_write_headers': order_line_write_headers, 
    'stock_write_headers': stock_write_headers, 
    'stock_misc_headers': stock_misc_headers
}
