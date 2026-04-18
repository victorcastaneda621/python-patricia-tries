import time
import data_structures.patricia_trie.patricia_trie as pt
from general_utils import prune_dataset

def mine_patricia(transactions, min_supp):
    before_trie_build = time.perf_counter()

    transactions = prune_dataset(transactions, min_supp)

    trie = pt.PatriciaTrie()

    # Inserts the transactions and returns the counts of items
    count = trie.insert(transactions)

    IL = trie.index_to_item
    h,l = 0,0
    X = ["" for _ in IL]
    X_as_bit_seq = 0

    after_trie_build = time.perf_counter()

    returned = []
    while l<len(IL):
        if count[IL[l]] < min_supp:
            l += 1
        else:
            if h>0 and IL[l]==X[h-1]:        
                l += 1
                h -= 1
                X_as_bit_seq = X_as_bit_seq ^ (1 << trie.item_to_index[X[h]])  # remove the bit of the item we backtrack from
            else:
                X[h] = IL[l]
                X_as_bit_seq = X_as_bit_seq | (1 << l)
                h += 1
                #print("Generate","".join(X[:h]),X)
                returned.append(X[:h])

                for i in range(l-1,-1,-1):
                    count[IL[i]] = trie.get_support_of_itemset_as_bit_seq((1 << i) | X_as_bit_seq)
                l=0
    after_mining = time.perf_counter()
    node_count, max_depth = trie.count_nodes_and_max_depth()
    return {"build_time": after_trie_build - before_trie_build,
            "mining_time": after_mining - after_trie_build,
            "itemsets": returned,
            "node_count": node_count,
            "max_depth": max_depth}