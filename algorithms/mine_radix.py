from data_structures import radix_tree_SN_TD, radix_tree_SN_BU, radix_tree_MN_TD, radix_tree_MN_BU
from data_structures.radix_tree.radix_tree_utils import radix_tree_count_sort
from general_utils import prune_dataset

def mine_radix(transactions, min_supp, single_node: bool, top_down: bool, benchmark= False):

    transactions = prune_dataset(transactions, min_supp)

    if single_node:
        if top_down:
            tree = radix_tree_SN_TD.RadixTree_SN_TD()
        else:
            tree = radix_tree_SN_BU.RadixTree_SN_BU()
    else:
        if top_down:
            tree = radix_tree_MN_TD.RadixTree_MN_TD()
        else:
            tree = radix_tree_MN_BU.RadixTree_MN_BU()

    transactions, count, order = radix_tree_count_sort(transactions)
    tree.insert(transactions)

    IL = list(order.keys())
    h,l = 0,0
    X = ["" for _ in IL]

    returned = []
    while l<len(IL):
        if count[IL[l]] < min_supp:
            l += 1
        else:
            if h>0 and IL[l]==X[h-1]:
                l += 1
                h -= 1
            else:
                X[h] = IL[l]
                h += 1
                if not benchmark:
                    returned.append(X[:h])

                for i in range(l-1,-1,-1):
                    count[IL[i]] = tree.get_support_of_itemset(X[:h] + [IL[i]], order)
                l=0
    print("itemsets:", str(len(returned)))
    
    return {"build_time": "-",
            "mining_time": "-",
            "itemsets": returned,
            "node_count": "-",
            "max_depth": "-",
            "peak_memory_mb": "-",
            "tree_size_mb":"-"
            }
