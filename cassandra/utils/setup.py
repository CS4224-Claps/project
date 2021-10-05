def setup(session, schema_file):
    """
    Initialises the database.
    """
    statements = read_cql_statements(schema_file)
    for statement in statements:
        session.execute(read_cql_statements(schema_file))

def read_cql_statements(file):
    """
    Returns a list of cql statements found in the input file.
    """
    with open(file, "r") as f:
        text = f.read()
        statements = text.split(";")
        return [statement + ";" for statement in statements if statement.strip()]
