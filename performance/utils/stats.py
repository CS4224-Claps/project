import os

import numpy as np 


def get_client_num(file):
    filename = os.path.splitext(file)[0]
    client_num = filename.split("_")[0]
    return client_num


def get_stats(filename, xact_times):
    client_num = get_client_num(filename)
    num_xacts = len(xact_times)
    total_xact_time = np.sum(xact_times) / 1000.0
    xact_throughput = round(num_xacts / total_xact_time, 3)
    avg_xact_time = np.average(xact_times)
    median_xact_time = np.median(xact_times)
    nine_five_latency = np.percentile(xact_times, 95)
    nine_nine_latency = np.percentile(xact_times, 99)

    return client_num, num_xacts, total_xact_time, xact_throughput,\
        avg_xact_time, median_xact_time, nine_five_latency, nine_nine_latency


def get_throughputs(throughput_times):
    min_throughput = np.min(throughput_times)
    max_throughput = np.max(throughput_times)
    avg_throughput = np.average(throughput_times)

    return min_throughput, max_throughput, avg_throughput
