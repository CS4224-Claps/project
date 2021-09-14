import csv
import pandas as pd
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
        writer = csv.writer(f)
        writer.writerow(
            "client_num,tx_count,total_time,tx_throughput,avg_latency,median_latency,95th_latency,99th_latency"
        )
        writer.writerows(client_stats)
        f.close()


def print_throughput_stats(directory):
    throughput_stats = None

    with open(f"{directory}/clients.csv", "r") as f:
        clients_data = pd.read_csv(f, names=["N", "E", "T", "A", "M", "95", "99"])
        throughput_times = clients_data["T"].to_numpy()
        throughput_stats = get_throughputs(throughput_times)

    with open(f"{directory}/throughput.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow("min_throughput,max_throughput,avg_throughput")
        writer.writerow(throughput_stats)
        f.close()


def print_cockroach_stats(directory, conn):
    with open(f"{directory}/dbstate.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(
            "w_ytd",
            "d_ytd",
            "d_next_o_id",
            "c_balance",
            "c_ytd_payment",
            "c_payment_cnt",
            "c_delivery_cnt",
            "o_id",
            "o_ol_cnt",
            "ol_amount",
            "ol_quantity",
            "s_quantity",
            "s_ytd",
            "s_order_count",
            "s_remote_cnt",
        )
        writer.writerow(get_cockroach_stats(conn))
        f.close()
