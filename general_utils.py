import os, csv
from collections import Counter

def row_to_transaction(row):
    """Turns a row of data from a table into a transaction.

    Parameters
    ----------
    row
        The row of data from the table.

    Returns
    -------
    set()
        A set containing f"{col}={value}" for every column of data.

    """
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

def write_metrics(metrics: dict, file: str):
    """Writes a dictionary of metrics to a file.

    Parameters
    ----------
    metrics
        metric_name:metric_value dictionary. Metric names must stay consistent
        when writing on the same file several times.

    file
        Path of the file where the metrics are to be written.

    """
    file_exists = os.path.isfile(file)
    with open(file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(metrics)

def write_results(itemsets: list, args):
    """Writes the resulting itemsets from a mining operation to a text file.

    Parameters
    ----------
    itemsets : list
        List of items to write.

    args
        Namespace returned by Argparse. Used to customize the file name:
        f"files/results/{args.alg}_{args.data}_{args.minsup}.txt"

    """
    filename = f"files/results/{args.alg}_{args.data}_{args.minsup}.txt"
    with open(filename, "w") as f:
        for itemset in itemsets:
            f.write(",".join(itemset) + "\n")