import os
from data_structures import radix_tree_MN_BU
from data_structures.radix_tree.radix_tree_utils import radix_tree_count_sort
from general_utils import prune_dataset

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

i = 0
minsup = [640, 35000, 40535, 200, 14000]
for data in ["mushroom", "pumsb", "connect4", "artificial_1", "pumsb_star"]:
    transactions = load_dataset(data)

    avg_len_list = []
    longest = 0
    num = 0
    items = set()
    for t in transactions:
        leng = 0
        num += 1
        for item in t:
            leng += 1
            items.add(item)
        if leng > longest:
            longest = leng
        avg_len_list.append(leng)
    avg_len = sum(avg_len_list) / len(avg_len_list)
    item_num = len(items)
    print("-----PRE-------", data, "--------------------")
    print("|D|: ", num, " |I|: ", item_num, " max: ", longest, " avg_len: ", avg_len)

    transactions = prune_dataset(transactions, minsup[i])

    avg_len_list = []
    longest = 0
    num = 0
    items = set()
    for t in transactions:
        leng = 0
        num += 1
        for item in t:
            leng += 1
            items.add(item)
        if leng > longest:
            longest = leng
        avg_len_list.append(leng)
    avg_len = sum(avg_len_list) / len(avg_len_list)
    item_num = len(items)
    print("-----POST-------", data, "--------------------")
    print("|D|: ", num, " |I|: ", item_num, " max: ", longest, " avg_len: ", avg_len)

    td = radix_tree_MN_BU.RadixTree_MN_BU()
    transactions, count, order = radix_tree_count_sort(transactions)
    td.insert(transactions)
    print("nodes, max_depth: ", td.count_nodes_and_max_depth())
    print("--------------------------------")
    print("--------------------------------")
    i += 1
