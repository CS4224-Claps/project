def next_xact(f):
    io_line = f.readline()

    if io_line == "":  # EOF
        return None

    io_line = io_line.rstrip("\n").split(",")

    if io_line[0] != "N":
        return io_line[0], io_line

    data_lines = [f.readline().rstrip("\n").split(",") for _ in range(int(io_line[-1]))]
    return io_line[0], io_line, data_lines
