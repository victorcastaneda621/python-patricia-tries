from ucimlrepo import fetch_ucirepo
import argparse, os

from general_utils import write_metrics, write_results, row_to_transaction
from algorithms.mine_patricia import mine_patricia
from algorithms.mine_lists import mine_lists
from algorithms.mine_radix import mine_radix

ALGORITHMS = {
    "patricia": mine_patricia,
    "list": mine_lists,
    "radix": mine_radix
}

DATASETS = {
    "small_cities",
    "mushroom",
    "connect4",
    "pumsb",
    "connect4_fimi",
    "artificial_1",
    "mushroom_fimi"
}

METRICS_FILE = "files/metrics.csv"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Frequent Itemset Mining")
    parser.add_argument("--alg", choices=ALGORITHMS.keys(), 
                        required=True, help="Algorithm to run")
    parser.add_argument("--data", choices=DATASETS, 
                        required=True, help="Dataset to use")
    parser.add_argument("--minsup", type=int,
                        required=True, help="Minimun support")
    args = parser.parse_args()

    algorithm = ALGORITHMS[args.alg]

    ### dataset fetching ################################################################
    match args.data:
        case "small_cities":
            transactions = [{"Atenas", "Oslo", "Roma", "Viena"}, {"Oslo"}, 
                            {"Oslo", "Roma", "Viena"}, {"Oslo"}, {"Londres", "Madrid"}, 
                            {"Londres", "Madrid", "Oslo"}]
        case "mushroom":
            mushroom = fetch_ucirepo(id=73)
            dataset = mushroom.data.features
            transactions = [row_to_transaction(row) for _, row in dataset.iterrows()]
        case "connect4":
            connect_4 = fetch_ucirepo(id=26)
            dataset = connect_4.data.features
            transactions = [row_to_transaction(row) for _, row in dataset.iterrows()]
        case "pumsb":
            transactions = []
            with open("datasets/pumsb.dat") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    transactions.append({str(x) for x in line.split()})
        case "connect4_fimi":
            transactions = []
            with open("datasets/connect.dat") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    transactions.append({str(x) for x in line.split()})
        case "artificial_1":
            transactions = []
            with open("datasets/T10I4D100k.dat") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    transactions.append({str(x) for x in line.split()})
        case "mushroom_fimi":
            transactions = []
            with open("datasets/mushroom.dat") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    transactions.append({str(x) for x in line.split()})
    #####################################################################################

    results = algorithm(transactions, args.minsup) # Call the chosen miner
    metrics = {
        "algorithm": args.alg,
        "dataset": args.data,
        "minsup": args.minsup,
        "build_time": results["build_time"],
        "mining_time": results["mining_time"]
    }

    if not os.path.exists("files"): # Make sure the files directory exists
        os.makedirs("files")
        os.makedirs("files/results")

    write_metrics(metrics, METRICS_FILE) # Write metrics to CSV
    write_results(results["itemsets"], args) # Write mined itemsets to .txt
    print(str(results["build_time"] + results["mining_time"]) + " s")
