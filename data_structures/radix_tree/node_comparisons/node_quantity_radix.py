import data_structures.radix_tree.radix_tree_SN_TD as rtree_single_node
from data_structures.radix_tree.radix_tree_utils import radix_tree_count_sort
import random

def load_local_dataset(path):
    transactions = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                transactions.append({str(x) for x in line.split()})
    return transactions

for dataset in ["TEST"]:
    match dataset:
        case "TEST":
            transactions = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}]
        case "MUSHROOM":
            transactions = load_local_dataset("datasets/mushroom.dat")
        case "CONNECT4":
            transactions = load_local_dataset("datasets/connect.dat")
        case "PUMSB":
            transactions = load_local_dataset("datasets/pumsb.dat")
        case "PUMSB_STAR":
            transactions = load_local_dataset("datasets/pumsb_star.dat")
        case "T10I4D100K":
            transactions = load_local_dataset("datasets/T10I4D100K.dat")

    t_support, support, order = radix_tree_count_sort(transactions)
    print("|I|: ", len(order))

    t_alph = [sorted(list(t)) for t in transactions]

    all_items = list(set().union(*transactions))
    random_order = all_items[:]
    random.shuffle(random_order)
    item_to_priority = {item: i for i, item in enumerate(random_order)}
    t_random = [sorted(list(t), key=lambda x: item_to_priority[x]) for t in transactions]

    t_random_local = [random.sample(list(t), len(t)) for t in transactions]

    support_single = rtree_single_node.RadixTree_SN_TD()
    support_single.insert(t_support)

    alph_single = rtree_single_node.RadixTree_SN_TD()
    alph_single.insert(t_alph)

    random_single = rtree_single_node.RadixTree_SN_TD()
    random_single.insert(t_random)

    random_local = rtree_single_node.RadixTree_SN_TD()
    random_local.insert(t_random_local)

    print(f"{dataset} SINGLE-NODE (Total Nodes | Total Elements ) -------------------------------")
    print(f"Support:      {support_single.count_nodes_and_max_depth()[0]}" + " | " + str(support_single.count_total_elements()))
    print(f"Alphabetical: {alph_single.count_nodes_and_max_depth()[0]}" + " | " + str(alph_single.count_total_elements()))
    print(f"Random:       {random_single.count_nodes_and_max_depth()[0]}" + " | " + str(random_single.count_total_elements()))
    print(f"Random (local):       {random_local.count_nodes_and_max_depth()[0]}" + " | " + str(random_local.count_total_elements()))
