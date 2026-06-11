import heapq
from collections import Counter

def select(D, X):
    out = []
    X = set(X)
    for tran in D:
        if X.issubset(tran):
            out.append(tran)
    return out
 
def closure(D):
    """Intersection of all transactions, i.e. closure + its support."""
    if not D:
        return set(), 0
    return set.intersection(*[set(t) for t in D]), len(D)
 
def attempt_ppc_extensions(X, n, item_to_idx, item_order, D, sigma, Q):
    for j in range(1, n + 1):
        item = item_order[j - 1]
        if item in X:
            continue  # item j already in X, so item can't extend X

        D_Y = select(D, X | {item}) # Projection of D, over Y = X U item
        Y, supp_Y = closure(D_Y) # This returns Y = the closure of the projection,
        # so Y contains all items tha always appear with X U item

        if supp_Y < sigma: # The current extenson has support lower than our current
            # bound for sigma_K, so definitely won't have more than sigma_K support
            continue

        # We check that Y(j-1) = X(j-1), i.e. that the prefix of both itemsets
        # matches until item j-1.
        Y_prefix    = {a for a in Y   if item_to_idx[a] < j}
        x_prefix  = {a for a in X if item_to_idx[a] < j}
        if Y_prefix != x_prefix:
            continue # If they are not, then the extension added items before j
            # so we don't need to consider it

        # push (s, D_Y, core_i(Y), Y(core_i(Y)-1)) to the queue
        # core_i(X) = prefix of X until position j-1
        heapq.heappush(Q, (-supp_Y, D_Y, j, Y_prefix))
 
def mine_topk_lists(transactions, K, benchmark=False):

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

    count = Counter()
    for t in transactions:
        for item in t:
            count[item] += 1
    item_order = sorted(count.keys(), key=lambda a: count[a])
    n = len(item_order)
    item_to_idx = {a: i + 1 for i, a in enumerate(item_order)}

    sigma = 0 # Current lower bound for sigma_K,
    # sigma_K is the minsup that yields K itemsets, we don't know it
    sigma_prime = sigma # Working threshold / sigma we will use

    Q = [] # priority queue, we use negated support to order correctly
    extracted = 0
    returned = []

    current_closure, _ = closure(transactions)
    if current_closure: # i.e. it is not empty
        if not benchmark:
            returned.append(current_closure)
        extracted += 1
        if K == 1:
            sigma_prime = len(transactions)

    attempt_ppc_extensions(current_closure, n, 
                            item_to_idx, item_order, 
                            transactions, sigma, Q)
    while Q and -Q[0][0] >= sigma_prime: # Q[0] is the top of the queue
        supp_Y, D_Y, i, _ = heapq.heappop(Q)
        supp_Y = -supp_Y

        extracted += 1 # We extract the next closed itemset from the heap
        if extracted == K: 
            # If we have extracted enough items, we found the real minsup
            sigma_prime = supp_Y
        Y, _ = closure(D_Y)
        
        if Y in returned:
            extracted -= 1
            continue
        Y, _ = closure(D_Y)
        
        if not benchmark:
            returned.append(Y) # We need to return the new itemset in FC (Y)

        if supp_Y > sigma:
            for j in range(i+1, n+1):
                item_j = item_order[j - 1]

                if item_j in Y:
                    continue # Not an extension

                D_X = select(D_Y, Y | {item_j})
                X, supp_X = closure(D_X)

                X_prefix_j = {a for a in X if item_to_idx[a] < j}
                Y_prefix_j = {a for a in Y if item_to_idx[a] < j}
                if X_prefix_j == Y_prefix_j and supp_X >= sigma:
                    heapq.heappush(Q, (-supp_X, D_X, j, X_prefix_j))
                    remaining = K - extracted
                    if extracted + len(Q) >= K and remaining > 0:
                        # We can raise the lower bound
                        sigma = -heapq.nsmallest(K - extracted, Q)[-1][0]
                        Q = [e for e in Q if -e[0] >= sigma]
                        heapq.heapify(Q)

                        supp = Q[0][0]
                        while -supp < sigma:
                            heapq.heappop(Q)
                            supp = Q[0][0]
 
    return {
        "build_time": "-",
        "mining_time": "-",
        "itemsets": returned,
        "node_count": "-",
        "max_depth": "-",
        "peak_memory_mb": "-",
        "tree_size_mb": "-",
        "sigma": sigma
    }
