import csv
import pandas as pd
import numpy as np
from pathlib import Path

from utils.cockroach import get_cockroach_stats
from utils.stats import get_stats, get_throughputs


client_headers = ["xact", "exec_time"]

total_headers = [
    "client_num",
    "tx_count",
    "total_time",
    "tx_throughput",
    "avg_latency",
    "median_latency",
    "95th_latency",
    "99th_latency",
]


def print_client_stats(directory):
    client_stats = []

    for file in Path(directory).glob("*_info.csv"):
        xact_data = pd.read_csv(file, names=client_headers)
        xact_times = xact_data["exec_time"].to_numpy()
        client_stats.append(get_stats(file, xact_times))

    client_stats.sort(key=lambda stats: int(stats[0]))

    with open(f"{directory}/clients.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerows(client_stats)


def print_throughput_stats(directory):
    throughput_stats = None

    with open(f"{directory}/clients.csv", "r") as f:
        clients_data = pd.read_csv(f, names=total_headers)
        throughput_times = clients_data["tx_throughput"].to_numpy()
        throughput_stats = get_throughputs(throughput_times)

    with open(f"{directory}/throughput.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(throughput_stats)


def print_cockroach_stats(directory, conn):
    with open(f"{directory}/dbstate.csv", "w+") as f:
        writer = csv.writer(f)
        cockroach_stats = get_cockroach_stats(conn)
        writer.writerows(np.reshape(cockroach_stats, (-1, 1)))
