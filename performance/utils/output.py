import csv
import pandas as pd
import numpy as np
from pathlib import Path

from utils.cassandra import get_cassandra_stats
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


def print_summary_stats(directory):
    data_frames = []

    for file in Path(directory).glob("*_info.csv"):
        xact_data = pd.read_csv(file, names=client_headers)
        data_frames.append(xact_data)

    xact_data = pd.concat(data_frames)
    total_xact_data = xact_data.groupby(["xact"])

    total_xact_data["exec_time"].describe(
        percentiles=[0.25, 0.5, 0.75, 0.95, 0.99]
    ).round(3).to_csv(f"{directory}/xacts.csv")


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


def print_cassandra_stats(directory, conn):
    with open(f"{directory}/dbstate.csv", "w+") as f:
        writer = csv.writer(f)
        cassandra_stats = get_cassandra_stats(conn)
        writer.writerows(np.reshape(cassandra_stats, (-1, 1)))
