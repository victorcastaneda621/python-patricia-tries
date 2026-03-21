from ucimlrepo import fetch_ucirepo
import argparse, os

from general_utils import write_metrics, write_results, row_to_transaction
from algorithms.mine_patricia import mine_patricia
from algorithms.mine_lists import mine_lists
from algorithms.mine_radix import mine_radix

ALGORITHMS = {
    "patricia": mine_patricia,
    "list": mine_lists,
    "radix": lambda t, m: mine_radix(t, m, single_node=False),
    "radix-single-node": lambda t, m: mine_radix(t, m, single_node=True)
}

DATASETS = [
    "small_cities",
    "mushroom",
    "connect4",
    "pumsb",
    "connect4_fimi",
    "artificial_1",
    "mushroom_fimi"
]

METRICS_FILE = "files/metrics.csv"

def load_local_dataset(path):
    transactions = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                transactions.append({str(x) for x in line.split()})
    return transactions

def load_dataset(name):
    match name:
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
            transactions = load_local_dataset("datasets/pumsb.dat")
        case "connect4_fimi":
            transactions = load_local_dataset("datasets/connect.dat")
        case "artificial_1":
            transactions = load_local_dataset("datasets/T10I4D100k.dat")
        case "mushroom_fimi":
            transactions = load_local_dataset("datasets/mushroom.dat")
        case _:
            raise ValueError(f"Unknown dataset: {name}")
    return transactions

def run_experiment(args):
    transactions = load_dataset(args.data)
    algorithm = ALGORITHMS[args.alg]

    results = algorithm(transactions, args.minsup) # Call the chosen miner

    metrics = {
        "algorithm": args.alg,
        "dataset": args.data,
        "minsup": args.minsup,
        "build_time": results["build_time"],
        "mining_time": results["mining_time"],
        "node_count": results["node_count"],
        "max_depth": results["max_depth"],
        "number_itemsets": len(results["itemsets"])
    }

    # Make sure the files directory exists
    os.makedirs("files", exist_ok=True)
    os.makedirs("files/results", exist_ok=True)

    write_metrics(metrics, METRICS_FILE) # Write metrics to CSV
    if args.save_results:
        write_results(results["itemsets"], args) # Write mined itemsets to .txt
    print(
        "Build time: " + str(results["build_time"]) + " s" +
        "\nMining time: " + str(results["mining_time"]) + " s" +
        "\nTotal time: " + str(results["build_time"] + results["mining_time"]) + " s" +
        "\nNumber of frequent itemsets: " + str(len(results["itemsets"]))
        )
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Frequent Itemset Mining")
    parser.add_argument("--alg", choices=ALGORITHMS.keys(), 
                        required=True, help="Algorithm to run")
    parser.add_argument("--data", choices=DATASETS, 
                        required=True, help="Dataset to use")
    parser.add_argument("--minsup", type=int,
                        required=True, help="Minimun support")
    parser.add_argument("--save-results", action="store_true",
                        default=False, help="Save results to .txt file")
    args = parser.parse_args()

    run_experiment(args)
