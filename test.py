from ucimlrepo import fetch_ucirepo
import argparse, csv, os

import transaction_to_bit_seq as tbs
from mine_patricia import mine_patricia
from mine_lists import mine_lists

def write_metrics(metrics):

    file_exists = os.path.isfile("files/metrics.csv")

    with open("files/metrics.csv", "a", newline="") as f:
        writer = csv.DictWriter(f,
            fieldnames=[
                "algorithm",
                "dataset",
                "minsup",
                "build_time",
                "mining_time"])

        if not file_exists:
            writer.writeheader()

        writer.writerow(metrics)

def write_results(itemsets):
    filename = f"files/results/{args.alg}_{args.data}_{args.minsup}.txt"
    with open(filename, "w") as f:
        for itemset in itemsets:
            f.write(",".join(itemset) + "\n")

ALGORITHMS = {
    "patricia": mine_patricia,
    "list": mine_lists
}

DATASETS = {
    "small_cities",
    "mushroom",
    "connect4"
}


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
            transactions = [tbs.row_to_transaction(row) for _, row in dataset.iterrows()]
        case "connect4":
            connect_4 = fetch_ucirepo(id=26)
            dataset = connect_4.data.features
            transactions = [tbs.row_to_transaction(row) for _, row in dataset.iterrows()]
    #####################################################################################

    results = algorithm(transactions, args.minsup) # Call the miner
    metrics = {
        "algorithm": args.alg,
        "dataset": args.data,
        "minsup": args.minsup,
        "build_time": results["build_time"],
        "mining_time": results["mining_time"]
    }

    if not os.path.exists("files"):
        os.makedirs("files")
        os.makedirs("files/results")

    write_metrics(metrics) # Write metrics to CSV
    write_results(results["itemsets"]) # Write mined itemsets to .txt
