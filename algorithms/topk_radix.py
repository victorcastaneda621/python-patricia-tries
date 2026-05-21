import heapq

from data_structures import radix_tree_SN_TD, radix_tree_SN_BU, radix_tree_MN_TD, radix_tree_MN_BU
from data_structures.radix_tree.radix_tree_utils import radix_tree_count_sort
 
def attempt_ppc_extensions(X, n, tree, order_to_item, item_to_order, sigma, Q):
    for j in range(1, n + 1):
        item = order_to_item[j - 1]
        if item in X:
            continue  # item j already in X, so item can't extend X

        # This returns Y = the closure of the projection,
        # so Y contains all items tha always appear with X U item
        itemset = [item] + [i for i in X if item_to_order[i] < item_to_order[item]]
        supp_Y, ppc_ok, Y = tree.get_support_ppc_and_closure(itemset, item_to_order)

        if supp_Y < sigma or not ppc_ok: 
            # The current extenson has support lower than our current
            # bound for sigma_K, so definitely won't have more than sigma_K support
            continue

        # push (s, D_Y, core_i(Y), Y(core_i(Y)-1)) to the queue
        # core_i(X) = prefix of X until position j-1
        heapq.heappush(Q, (-supp_Y, Y, j, None))
 
def mine_topk_radix(transactions, K, single_node: bool, top_down: bool):

    if K == 0:
        return {"itemsets": []}

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

    transactions, a, item_to_order = radix_tree_count_sort(transactions)
    order_to_item = list(item_to_order.keys())

    tree.insert(transactions)

    n = len(order_to_item)

    sigma = 0 # Current lower bound for sigma_K,
    # sigma_K is the minsup that yields K itemsets, we don't know it
    sigma_prime = sigma # Working threshold / sigma we will use

    Q = [] # priority queue, we use negated support to order correctly
    extracted = 0
    returned = []

    _, _, current_closure = tree.get_support_ppc_and_closure([], item_to_order)
    if current_closure: # i.e. it is not empty
        returned.append(current_closure)
        extracted += 1
        if K == 1:
            sigma_prime = len(transactions)

    attempt_ppc_extensions(current_closure, n, tree, order_to_item, item_to_order, sigma, Q)
    while Q and -Q[0][0] >= sigma_prime: # Q[0] is the top of the queue
        supp_Y, Y, i, _ = heapq.heappop(Q)
        supp_Y = -supp_Y

        extracted += 1 # We extract the next closed itemset from the heap
        if extracted == K: 
            # If we have extracted enough items, we found the real minsup
            sigma_prime = supp_Y
        returned.append(Y) # We need to return the new itemset in FC (Y)

        if supp_Y > sigma:
            for j in range(i+1, n+1):
                item_j = order_to_item[j - 1]
                if item_j in Y:
                    continue

                itemset = [item_j] + [i for i in Y if item_to_order[i] < item_to_order[item_j]]
                supp_X, ppc_ok, X = tree.get_support_ppc_and_closure(itemset, item_to_order)

                if supp_X >= sigma and ppc_ok:
                    heapq.heappush(Q, (-supp_X, X | {item_j}, j, None))
                    remaining = K - extracted
                    if extracted + len(Q) >= K and remaining > 0:
                        sigma = -heapq.nsmallest(remaining, Q)[-1][0]
                        Q = [e for e in Q if -e[0] >= sigma]
                        heapq.heapify(Q)
 
    return {"itemsets": returned}