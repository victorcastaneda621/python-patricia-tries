import heapq
import time
import tracemalloc
import sys, os

from data_structures import radix_tree_SN_TD, radix_tree_SN_BU, radix_tree_MN_TD, radix_tree_MN_BU
from data_structures.radix_tree.radix_tree_utils import radix_tree_count_sort

sys.path.append(os.path.expanduser("~/.local/lib/python3.6/site-packages"))
from pympler import asizeof
 
def attempt_ppc_extensions(X, n, item_order, tree, order, sigma, Q):
    for j in range(1, n + 1):
        item = item_order[j - 1]
        if item in X:
            continue  # item j already in X, so item can't extend X

        # This returns Y = the closure of the projection,
        # so Y contains all items tha always appear with X U item
        itemset = sorted(X | {item}, key=lambda a: order[a], reverse=True)
        supp_Y, ppc_ok, Y = tree.get_support_ppc_and_closure(itemset, order)

        if supp_Y < sigma or not ppc_ok: 
            # The current extenson has support lower than our current
            # bound for sigma_K, so definitely won't have more than sigma_K support
            continue

        # push (s, D_Y, core_i(Y), Y(core_i(Y)-1)) to the queue
        # core_i(X) = prefix of X until position j-1
        heapq.heappush(Q, (-supp_Y, Y, j, None))
 
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

    _, _, current_closure = tree.get_support_ppc_and_closure([], order)
    if current_closure: # i.e. it is not empty
        returned.append(current_closure)
        extracted += 1
        if K == 1:
            sigma_prime = len(transactions)

    attempt_ppc_extensions(current_closure, n, item_order, tree, order, sigma, Q)
    while Q and -Q[0][0] >= sigma_prime: # Q[0] is the top of the queue
        supp_Y, Y, i, _ = heapq.heappop(Q)
        supp_Y = -supp_Y

        extracted += 1 # We extract the next closed itemset from the heap
        if extracted == K: 
            # If we have extracted enough items, we found the real minsup
            sigma_prime = supp_Y
        returned.append(Y) # We need to return the new itemset in FC (Y)

        if supp_Y > sigma:
            Y_set = set(Y)
            for j in range(i+1, n+1):
                item_j = item_order[j - 1]
                if item_j in Y_set:
                    continue

                itemset = sorted(Y | {item_j}, key=lambda a: order[a], reverse=True)
                supp_X, ppc_ok = tree.get_support_and_ppc_check(itemset, order)

                if supp_X >= sigma and ppc_ok:
                    heapq.heappush(Q, (-supp_X, Y | {item_j}, j, None))
                    remaining = K - extracted
                    if extracted + len(Q) >= K and remaining > 0:
                        sigma = -heapq.nsmallest(remaining, Q)[-1][0]
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

"""Here is exactly why your topk_lists.py is >10x faster, and how you can optimize the Radix version.
1. The Pure Python vs. C-Extension Battle (The Main Culprit)

In topk_lists.py, your heavy lifting is done by two functions:

    X.issubset(tran)

    set.intersection(*[set(t) for t in D])

Even though you are writing Python, these specific set operations are implemented in highly optimized C code under the hood. They run at bare-metal speeds, bypassing Python's object overhead.

In topk_radix.py, every time you traverse the tree to check support or closures, you are executing pure Python bytecode. You are navigating objects, chasing pointers, making function calls, and doing dictionary/list lookups for child nodes. The CPU overhead of Python object management completely swallows the algorithmic advantages of the tree.
2. The Sorting Bottleneck in the Hot Loop

In mine_topk_radix, inside your innermost for loop, you have this line:
Python

itemset = sorted(Y | {item_j}, key=lambda a: order[a], reverse=True)

You are taking a set, unioning it, and then performing a full Timsort with a custom lambda function (which adds a Python function call overhead to every single comparison during the sort). You are doing this thousands of times per second.

How to optimize it: Since Y is presumably already sorted (or can be maintained as a sorted list), and you are only adding one item (item_j), do not use sorted(). Use the bisect module to insert item_j into a list in O(N) time, or maintain the itemsets in a way that respects the order natively without lambda functions.
3. The Heap Rebuild Penalty

Look at how both algorithms update sigma when the queue gets large:
Python

sigma = -heapq.nsmallest(remaining, Q)[-1][0]
Q = [e for e in Q if -e[0] >= sigma]
heapq.heapify(Q)

You are running nsmallest (which takes O(NlogK)), followed by a full list comprehension, followed by an O(N) heapify. You are doing this every single time a new valid extension is found and the queue is full.

How to optimize it:
If you just need to drop elements that fall below the new sigma, you don't need nsmallest every time. Since you only care about maintaining the top K elements, consider keeping Q at exactly size K using heapq.heappushpop(). This forces the heap to self-manage its size efficiently in C, rather than you manually rebuilding it in Python.
4. Delayed Closure Processing vs. Double Traversal

In topk_lists.py, your closure(D_Y) function gives you both the itemset closure and its support in one swift C-level sweep.

In topk_radix.py, you have to traverse the tree to check supp_Y, ppc_ok = tree.get_support_and_ppc_check(...). Then, if it passes, you traverse the tree again later with Y, _ = tree.get_closure(itemset_Y, order).

How to optimize it:
If possible, modify your Radix Tree's get_support_and_ppc_check to return the closure at the same time. If it's already at the correct node in the tree to know the support, it should be able to look at the node's lineage/children to determine the closure without starting a second traversal from the root."""