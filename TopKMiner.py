import argparse, os

from general_utils import write_metrics, write_results
from algorithms.topk_patricia import mine_topk_patricia
from algorithms.topk_lists import mine_topk_lists
from algorithms.topk_radix import mine_topk_radix

ALGORITHMS = {
    "patricia": mine_topk_patricia,
    "list": mine_topk_lists,
    "radix-SN-BU": lambda t, m: mine_topk_radix(t, m, single_node=True, top_down=False),
    "radix-SN-TD": lambda t, m: mine_topk_radix(t, m, single_node=True, top_down=True),
    "radix-MN-BU": lambda t, m: mine_topk_radix(t, m, single_node=False, top_down=False),
    "radix-MN-TD": lambda t, m: mine_topk_radix(t, m, single_node=False, top_down=True)
}

DATASETS = [
    "small_cities",
    "mushroom",
    "connect4",
    "pumsb",
    "pumsb_star",
    "artificial_1",
]

METRICS_FILE = "files/metrics_topk.csv"

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
        case "pumsb":
            transactions = load_local_dataset(os.path.join("datasets", "pumsb.dat"))
        case "connect4":
            transactions = load_local_dataset(os.path.join("datasets", "connect.dat"))
        case "artificial_1":
            transactions = load_local_dataset(os.path.join("datasets", "T10I4D100K.dat"))
        case "mushroom":
            transactions = load_local_dataset(os.path.join("datasets", "mushroom.dat"))
        case "pumsb_star":
            transactions = load_local_dataset(os.path.join("datasets", "pumsb_star.dat"))
        case _:
            raise ValueError(f"Unknown dataset: {name}")
    return transactions

def run_experiment(args):
    transactions = load_dataset(args.data)
    algorithm = ALGORITHMS[args.alg]

    results = algorithm(transactions, args.k) # Call the chosen miner

    metrics = {
        "algorithm": getattr(args, "alg", "-"),
        "dataset": getattr(args, "data", "-"),
        "k": getattr(args, "k", "-"),
        "build_time": results.get("build_time", "-"),
        "mining_time": results.get("mining_time", "-"),
        "total_time": results.get("mining_time", "-") + results.get("build_time", "-"),
        "node_count": results.get("node_count", "-"),
        "max_depth": results.get("max_depth", "-"),
        "peak_mem_mb": results.get("peak_memory_mb", "-"),
        "size_mb": results.get("tree_size_mb", "-"),
        "number_itemsets": len(results["itemsets"]) if "itemsets" in results else "-",
        "sigma": results.get("sigma", "-")
    }

    # Make sure the files directory exists
    os.makedirs("files", exist_ok=True)
    os.makedirs("files/results", exist_ok=True)

    write_metrics(metrics, METRICS_FILE) # Write metrics to CSV
    if not args.benchmark:
        write_results(results["itemsets"], args, "TopKMiner") # Write mined itemsets to .txt
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Closed Frequent Itemset Mining")
    parser.add_argument("--alg", choices=ALGORITHMS.keys(), 
                        required=True, help="Algorithm to run")
    parser.add_argument("--data", choices=DATASETS, 
                        required=True, help="Dataset to use")
    parser.add_argument("--k", type=int,
                        required=True, help="Number of itemsets to mine")
    parser.add_argument("--benchmark", action="store_true", 
                        help="Run in benchmark mode (skip saving results)")
    args = parser.parse_args()

    run_experiment(args)
