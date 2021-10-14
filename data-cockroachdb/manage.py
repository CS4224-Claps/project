import pandas as pd
import csv 

from utils.mappings import (
    file_names, 
    fileserver_name
)
from utils.raw_headers import raw_header_mappings 
from utils.dist_headers import dist_header_mappings

headers: {
    'warehouse': ['warehouse_read_headers', 'warehouse_write_headers'], 
    'district': ['district_read_headers', 'district_write_headers'], 
    'customer': ['customer_read_headers', 'customer_write_headers', 'customer_misc_headers'], 
    'order': ['order_read_headers', 'order_write_headers'], 
    'item': ['item_read_headers', 'item_misc_headers'], 
    'order-line': ['order_line_read_headers', 'order_line_write_headers'], 
    'stock': ['stock_write_headers', 'stock_misc_headers'],
}


file_address = fileserver_name.format('a')
xacts = pd.read_csv(file_address, names=['a', 'b', 'c'])
print(xacts)

"""
xacts = pd.read_csv("/home/seanlowjk/Git/project/cockroachdb-dist/a.csv", names=['a', 'b', 'c'])
print(xacts)
print(xacts[['a', 'b']])
xacts[['a', 'b']].to_csv("/home/seanlowjk/Git/project/cockroachdb-dist/b.csv", index=False, header=False)
"""
