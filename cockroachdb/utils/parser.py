def parse(io_line, data_lines=[]):
    io_line = io_line.split(",")
    data_lines = [line.split(",") for line in data_lines]
    return io_line, data_lines
