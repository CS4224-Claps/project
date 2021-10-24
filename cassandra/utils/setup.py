import csv
import os
import shutil
import subprocess

from collections import defaultdict

LOAD_WAREHOUSE = "COPY wholesale.Warehouse (W_ID, W_NAME, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP, W_TAX, W_YTD) FROM '{}';"
LOAD_DISTRICT = "COPY wholesale.District (D_W_ID, D_ID, D_NAME, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, D_TAX, D_YTD, D_NEXT_O_ID, W_TAX) FROM '{}';"
LOAD_CUSTOMER = "COPY wholesale.Customer (C_W_ID, C_D_ID, C_ID, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DELIVERY_CNT, C_DATA, W_NAME, D_NAME) FROM '{}';"
LOAD_ORDER = "COPY wholesale.Orders (O_W_ID, O_D_ID, O_ID, O_C_ID, O_CARRIER_ID, O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D) FROM '{}' WITH NULL = 'null';"
LOAD_ITEM = "COPY wholesale.Item (I_ID, I_NAME, I_PRICE, I_IM_ID, I_DATA) FROM '{}';"
LOAD_ORDERLINE = "COPY wholesale.OrderLine (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER, OL_I_ID, OL_DELIVERY_D, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO, I_NAME) FROM '{}' WITH NULL = 'null';"
LOAD_STOCK = "COPY wholesale.Stock (S_W_ID, S_I_ID, S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT, S_DIST_01, S_DIST_02, S_DIST_03, S_DIST_04, S_DIST_05, S_DIST_06, S_DIST_07, S_DIST_08, S_DIST_09, S_DIST_10, S_DATA, I_PRICE, I_NAME) FROM '{}';"

TEMP = 'temp'
WAREHOUSE = 'warehouse.csv'
DISTRICT = 'district.csv'
CUSTOMER = 'customer.csv'
ORDER = 'order.csv'
ITEM = 'item.csv'
ORDERLINE = 'order-line.csv'
STOCK = 'stock.csv'

def setup(session, schema_file, data_folder):
    """
    Initialises the database.
    """
    create_temp_folder()
    create_tables(session, schema_file)
    add_duplicated_fields(data_folder)
    load_data(data_folder)
    del_temp_folder()

def create_tables(session, schema_file):
    """
    Initialises tables.
    """
    statements = read_cql_statements(schema_file)
    for statement in statements:
        session.execute(statement, timeout=999)

def read_cql_statements(file):
    """
    Returns a list of cql statements found in the input file.
    """
    with open(file, "r") as f:
        text = f.read()
        statements = text.split(";")
        return [statement + ";" for statement in statements if statement.strip()]

def add_duplicated_fields(data_folder):
    """
    Creates a temporary local csv copy for tables which require additional fields.
    """
    add_wtax_to_district(data_folder)
    add_iprice_and_iname_to_stock(data_folder)
    add_iname_to_orderline(data_folder)
    add_wname_and_dname_to_customer(data_folder)

def add_wtax_to_district(data_folder):
    add_attrs_to_table(os.path.join(data_folder, WAREHOUSE),
                       os.path.join(data_folder, DISTRICT),
                       os.path.join(TEMP, DISTRICT),
                       [0], [0], [7])

def add_iprice_and_iname_to_stock(data_folder):
    add_attrs_to_table(os.path.join(data_folder, ITEM),
                       os.path.join(data_folder, STOCK),
                       os.path.join(TEMP, STOCK),
                       [0], [1], [2, 1])

def add_iname_to_orderline(data_folder):
    add_attrs_to_table(os.path.join(data_folder, ITEM),
                       os.path.join(data_folder, ORDERLINE),
                       os.path.join(TEMP, ORDERLINE),
                       [0], [4], [1])

def add_wname_and_dname_to_customer(data_folder):
    add_attrs_to_table(os.path.join(data_folder, WAREHOUSE),
                       os.path.join(data_folder, CUSTOMER),
                       os.path.join(TEMP, 'temp' + CUSTOMER),
                       [0], [0], [1])
    add_attrs_to_table(os.path.join(data_folder, DISTRICT),
                       os.path.join(TEMP, 'temp' + CUSTOMER),
                       os.path.join(TEMP, CUSTOMER),
                       [0, 1], [0, 1], [2])

def add_attrs_to_table(from_csv, to_csv, new_csv, from_pk_indices, to_pk_indices, attr_indices):
    """
    Creates a copy (new_csv) of the to_csv with additional attributes from the from_csv.
    """
    with open(from_csv, 'r') as from_table, open(to_csv, 'r') as to_table, open(new_csv, 'w') as new_table:
        from_reader = csv.reader(from_table)
        # Create a map of the primary key to [additional attributes]
        pk_attr_map = {}
        for row in from_reader:
            pk_attr_map[tuple(row[pk_index] for pk_index in from_pk_indices)] = [row[attr_index] for attr_index in attr_indices]
        to_reader = csv.reader(to_table)
        to_writer = csv.writer(new_table)
        for row in to_reader:
            pk = tuple(row[pk_index] for pk_index in to_pk_indices)
            attrs = pk_attr_map[pk]
            row.extend(attrs)
            to_writer.writerow(row)

def load_data(data_folder):
    """
    Loads data from the data_folder for unmodified csvs, and the TEMP folder for modified csvs.
    This uses the COPY command which is only usable in cqlsh, not via the python driver.
    """
    cmd = ['cqlsh', 'xcnd35']
    subprocess.run(cmd, input=LOAD_WAREHOUSE.format(os.path.join(data_folder, WAREHOUSE)), encoding='utf-8')
    subprocess.run(cmd, input=LOAD_DISTRICT.format(os.path.join(TEMP, DISTRICT)), encoding='utf-8')
    subprocess.run(cmd, input=LOAD_CUSTOMER.format(os.path.join(TEMP, CUSTOMER)), encoding='utf-8')
    subprocess.run(cmd, input=LOAD_ORDER.format(os.path.join(data_folder, ORDER)), encoding='utf-8')
    subprocess.run(cmd, input=LOAD_ITEM.format(os.path.join(data_folder, ITEM)), encoding='utf-8')
    subprocess.run(cmd, input=LOAD_ORDERLINE.format(os.path.join(TEMP, ORDERLINE)), encoding='utf-8')
    subprocess.run(cmd, input=LOAD_STOCK.format(os.path.join(TEMP, STOCK)), encoding='utf-8')

def create_temp_folder():
    if not os.path.isdir(TEMP):
        os.mkdir(TEMP)

def del_temp_folder():
    shutil.rmtree(TEMP)
