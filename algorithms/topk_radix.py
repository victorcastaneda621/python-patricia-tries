import heapq
import time
import tracemalloc
import sys, os

from data_structures import radix_tree_SN_TD, radix_tree_SN_BU, radix_tree_MN_TD, radix_tree_MN_BU
from data_structures.radix_tree.radix_tree_utils import radix_tree_count_sort

sys.path.append(os.path.expanduser("~/.local/lib/python3.6/site-packages"))
from pympler import asizeof
 
def attempt_ppc_extensions(X, n, item_to_idx, item_order, tree, order, sigma, Q):
    for j in range(1, n + 1):
        item = item_order[j - 1]
        if item in X:
            continue  # item j already in X, so item can't extend X

        # This returns Y = the closure of the projection,
        # so Y contains all items tha always appear with X U item
        Y, supp_Y = tree.get_closure(sorted(X | {item}, key=lambda a: order[a], reverse=True), order)

        if supp_Y < sigma: # The current extenson has support lower than our current
            # bound for sigma_K, so definitely won't have more than sigma_K support
            continue

        # We check that Y(j-1) = X(j-1), i.e. that the prefix of both itemsets
        # matches until item j-1.
        Y_prefix    = {a for a in Y   if item_to_idx[a] < j}
        bot_prefix  = {a for a in X if item_to_idx[a] < j}
        if Y_prefix != bot_prefix:
            continue # If they are not, then the extension added items before j
            # so we don't need to consider it

        # push (s, D_Y, core_i(Y), Y(core_i(Y)-1)) to the queue
        # core_i(X) = prefix of X until position j-1
        heapq.heappush(Q, (-supp_Y, Y, j, Y_prefix))
 
def mine_topk_radix(transactions, K, single_node: bool, top_down: bool):
    before_build = time.perf_counter()
    # tracemalloc.start() # MEM

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

    transactions, _, order = radix_tree_count_sort(transactions)
    tree.insert(transactions)

    if K == 0:
        return {
        "build_time": 0,
        "mining_time": 0,
        "itemsets": [],
        "node_count": "-",
        "max_depth": "-",
        "peak_memory_mb": "-",
        "tree_size_mb": "-",
    }

    item_to_idx = {a: order[a] + 1 for a in order}
    item_order = sorted(order.keys(), key=lambda a: order[a])
    n = len(item_order)

    after_build = time.perf_counter()

    #list_size_bytes = asizeof.asizeof(transactions) # MEM
    #list_size_mb = list_size_bytes / (1024 * 1024) # MEM
    #print("tree_size_mb:" + str(list_size_mb)) # MEM

    sigma = 0 # Current lower bound for sigma_K,
    # sigma_K is the minsup that yields K itemsets, we don't know it
    sigma_prime = sigma # Working threshold / sigma we will use

    Q = [] # priority queue, we use negated support to order correctly
    extracted = 0
    returned = []

    current_closure, _ = tree.get_closure([], order)
    if current_closure: # i.e. it is not empty
        returned.append(current_closure)
        extracted += 1
        if K == 1:
            sigma_prime = len(transactions)

    attempt_ppc_extensions(current_closure, n, 
                            item_to_idx, item_order, 
                            tree, order, sigma, Q)
    while Q and -Q[0][0] >= sigma_prime: # Q[0] is the top of the queue
        supp_Y, Y, i, Y_prefix = heapq.heappop(Q)
        supp_Y = -supp_Y

        extracted += 1 # We extract the next closed itemset from the heap
        if extracted == K: 
            # If we have extracted enough items, we found the real minsup
            sigma_prime = supp_Y
        returned.append(Y) # We need to return the new itemset in FC (Y)

        if supp_Y > sigma:
            for j in range(i+1, n+1):
                item_j = item_order[j - 1]

                if item_j in Y:
                    continue # Not an extension

                X, supp_X = tree.get_closure(sorted(Y | {item_j}, key=lambda a: order[a], reverse=True), order)

                X_prefix_j = {a for a in X if item_to_idx[a] < j}
                Y_prefix_j = {a for a in Y if item_to_idx[a] < j}
                if X_prefix_j == Y_prefix_j and supp_X >= sigma:
                    heapq.heappush(Q, (-supp_X, X, j, X_prefix_j))
                    remaining = K - extracted
                    if extracted + len(Q) >= K and remaining > 0:
                        # We can raise the lower bound
                        sigma = -heapq.nsmallest(K - extracted, Q)[-1][0]
                        Q = [e for e in Q if -e[0] >= sigma]
                        heapq.heapify(Q)

    after_mining = time.perf_counter()
    #_, peak = tracemalloc.get_traced_memory() # MEM
    #peak_memory_mb = peak / (1024 * 1024) # MEM
    #tracemalloc.stop() # MEM
 
    return {
        "build_time": after_build - before_build,
        "mining_time": after_mining - after_build,
        "itemsets": returned,
        "node_count": "-",
        "max_depth": "-",
        "peak_memory_mb": "-",
        "tree_size_mb": "-",
    }
