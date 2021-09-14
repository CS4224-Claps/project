
import glob
import os 
import csv 

import pandas as pd 

from utils.stats import get_stats, get_throughputs

def print_client_stats(cwd, indir, outdir):
    os.chdir(cwd)
    os.chdir(indir)
    client_stats = []

    for file in glob.glob("*.csv"):
        xact_data = pd.read_csv(file, names=["Xact", "Time"])
        xact_times = xact_data["Time"].to_numpy()
        client_stats.append(get_stats(file, xact_times))

    os.chdir(cwd)

    with open(outdir + "/clients.csv", "w+") as f:
        writer = csv.writer(f)

        writer.writerows(client_stats)
        f.close()

def print_throughput_stats(cwd, outdir):
    os.chdir(cwd)

    throughput_stats = None 

    with open(outdir + "/clients.csv", "r") as f:
        clients_data = pd.read_csv(f, names=["N", "E", "T", "A", "M", "95", "99"])
        throughput_times = clients_data["T"].to_numpy()
        throughput_stats = get_throughputs(throughput_times)

    
    with open(outdir + "/throughput.csv", "w+") as f:
        writer = csv.writer(f)

        writer.writerow(throughput_stats)
        f.close()
