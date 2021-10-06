def setup(session, schema_file):
    """
    Initialises the database.
    """
    statements = read_cql_statements(schema_file)
    for statement in statements:
        session.execute(read_cql_statements(schema_file))
    add_duplicated_fields(session)

def read_cql_statements(file):
    """
    Returns a list of cql statements found in the input file.
    """
    with open(file, "r") as f:
        text = f.read()
        statements = text.split(";")
        return [statement + ";" for statement in statements if statement.strip()]

# there should be a better way to do it
def add_duplicated_fields(session):
    add_wtax_to_district(session)
    add_iprice_and_iname_to_stock(session)

def add_wtax_to_district(session):
    rows = session.execute("SELECT W_ID, W_TAX FROM wholesale.Warehouse;")
    for warehouse in rows:
        for d_id in range(1, 11):
            session.execute(f"UPDATE wholesale.District SET W_TAX = {warehouse.w_tax} WHERE D_W_ID = {warehouse.w_id} AND D_ID = {d_id}")

def add_iprice_and_iname_to_stock(session):
    rows = session.execute("SELECT I_ID, I_PRICE, I_NAME FROM wholesale.Item;")
    warehouses = session.execute("SELECT W_ID FROM wholesale.Warehouse;")
    for warehouse in warehouses:
        for item in rows:
            session.execute(f"UPDATE wholesale.Stock SET I_PRICE = {item.i_price}, I_NAME = '{item.i_name}' WHERE S_I_ID = {item.i_id} AND S_W_ID = {warehouse.w_id};")
