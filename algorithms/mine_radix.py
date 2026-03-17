import time
import data_structures.radix_tree.radix_tree as rtree
from general_utils import radix_tree_count_sort

def mine_radix(transactions, min_supp):
    before_trie_build = time.perf_counter()

    tree = rtree.RadixTree()

    # Inserts the transactions and returns the counts of items
    transactions, count, order = radix_tree_count_sort(transactions)
    tree.insert(transactions)

    IL = list(order.keys())
    h,l = 0,0
    X = ["" for _ in IL]

    after_trie_build = time.perf_counter()

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
                returned.append(X[:h])

                for i in range(l-1,-1,-1):
                    count[IL[i]] = tree.get_support_of_itemset(X[:h] + [IL[i]], order)
                l=0
    after_mining = time.perf_counter()
    return {"build_time": after_trie_build - before_trie_build,
            "mining_time": after_mining - after_trie_build,
            "itemsets": returned}
