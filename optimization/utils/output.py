import pandas as pd
from pathlib import Path


client_headers = ["xact", "exec_time"]

def print_client_stats(directory):
    data_frames = []

    for file in Path(directory).glob("*_info.csv"):
        xact_data = pd.read_csv(file, names=client_headers)
        data_frames.append(xact_data)

    xact_data = pd.concat(data_frames)
    total_xact_data = xact_data.groupby(['xact'])

    print(total_xact_data['exec_time'].describe().to_csv('sample.csv'))
