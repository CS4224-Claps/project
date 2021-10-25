def parse_xact(f):
    input_line = f.readline()

    if input_line == "":  # EOF
        return None

    input_arr = input_line.rstrip("\n").split(",")

    if input_arr[0] != "N":
        return input_arr[0], input_arr

    data_lines = [
        f.readline().rstrip("\n").split(",") for _ in range(int(input_arr[-1]))
    ]
    return input_arr[0], input_arr, data_lines
