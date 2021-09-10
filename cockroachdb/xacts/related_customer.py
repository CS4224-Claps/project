import logging

from utils.decorators import validate_command


@validate_command("R")
def execute(conn, io_line):
    # Retrieve Data from IO Line
    w_id, d_id, c_id = map(int, io_line[1:])

    with conn.cursor() as cur:
        pass

    conn.commit()
