import os, csv
from collections import Counter

def row_to_transaction(row):
    """Turns a row of data from a table into a transaction.
    # Parameters
    - row: The row of data from the table
    """
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

def write_metrics(metrics, file):
    """Writes a dictionary of metrics to a file.
    # Parameters
    - metrics: metric_name:metric_value dictionary
    - file: Output file
    """
    file_exists = os.path.isfile(file)
    with open(file, "a", newline="") as f:
        writer = csv.DictWriter(f,
            fieldnames=[
                "algorithm",
                "dataset",
                "minsup",
                "build_time",
                "mining_time",
                "node_count",
                "max_depth",
                "number_itemsets"])

        if not file_exists:
            writer.writeheader()

        writer.writerow(metrics)

def write_results(itemsets, args):
    """Writes the itemsets to a file.
    # Parameters
    - itemsets: List of itemsets
    - args: Arguments used to generate the name of the file
        (files/results/{args.alg}_{args.data}_{args.minsup}.txt)
    """
    filename = f"files/results/{args.alg}_{args.data}_{args.minsup}.txt"
    with open(filename, "w") as f:
        for itemset in itemsets:
            f.write(",".join(itemset) + "\n")

def radix_tree_count_sort(transaction_list: list):
    support = Counter()
    for t in transaction_list:
        support.update(t)

    order = {item:i for i, (item, _) in enumerate(support.most_common())}

    for i in range(len(transaction_list)):
        transaction_list[i] = sorted(transaction_list[i], key=order.get)

    return transaction_list, support, order