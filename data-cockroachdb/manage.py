import pandas as pd
import csv 

from utils.mappings import (
    file_names, 
    fileserver_name
)
from utils.raw_headers import raw_header_mappings 
from utils.dist_headers import dist_header_mappings

raw_to_dist_mappings = {
    'warehouse': ['warehouse_read_headers', 'warehouse_write_headers'], 
    'district': ['district_read_headers', 'district_write_headers'], 
    'customer': ['customer_read_headers', 'customer_write_headers', 'customer_misc_headers'], 
    'order': ['order_read_headers', 'order_write_headers'], 
    'item': ['item_read_headers', 'item_misc_headers'], 
    'order-line': ['order_line_read_headers', 'order_line_write_headers'], 
    'stock': ['stock_write_headers', 'stock_misc_headers'],
}

for name in file_names: 
    file_address = fileserver_name.format(name)

    raw_headings = raw_header_mappings[name]
    data = pd.read_csv(file_address, , dtype=str, names=raw_headings)

    dist_heading_names = raw_to_dist_mappings[name]

    for heading in dist_heading_names: 
        dist_headings = dist_header_mappings[heading]
        dist_data = data[dist_headings]        

        dest_name = "{}.csv".format(heading)
        dist_data.to_csv(dest_name, mode="w+", index=False, header=False)
