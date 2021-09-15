import csv
import pandas as pd
import numpy as np
from pathlib import Path

from utils.cockroach import get_cockroach_stats
from utils.stats import get_stats, get_throughputs


def print_client_stats(directory):
    client_stats = []

    for file in Path(directory).glob("*.csv"):
        xact_data = pd.read_csv(file, names=["Xact", "Time"])
        xact_times = xact_data["Time"].to_numpy()
        client_stats.append(get_stats(file, xact_times))

    with open(f"{directory}/clients.csv", "w+") as f:
        headers = ["client_num","tx_count","total_time","tx_throughput",
            "avg_latency","median_latency","95th_latency","99th_latency"]
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(client_stats)
        f.close()


def print_throughput_stats(directory):
    throughput_stats = None

    with open(f"{directory}/clients.csv", "r") as f:
        clients_data = pd.read_csv(f)
        throughput_times = clients_data["tx_throughput"].to_numpy()
        throughput_stats = get_throughputs(throughput_times)

    with open(f"{directory}/throughput.csv", "w+") as f:
        headers = ["min_throughput","max_throughput","avg_throughput"]
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(throughput_stats)
        f.close()


def print_cockroach_stats(directory, conn):
    with open(f"{directory}/dbstate.csv", "w+") as f:
        writer = csv.writer(f)
        cockroach_stats =  get_cockroach_stats(conn)
        writer.writerows(np.reshape(cockroach_stats, (-1, 1)))
        f.close()
