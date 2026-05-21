import heapq
import data_structures.patricia_trie.patricia_trie as pt
 
def mine_topk_patricia(transactions, K):

    if K == 0:
        return {"itemsets": []}

    
    trie = pt.PatriciaTrie()

    trie.insert(transactions)

    sigma = 0 # Current lower bound for sigma_K,
    # sigma_K is the minsup that yields K itemsets, we don't know it
    sigma_prime = sigma # Working threshold / sigma we will use

    Q = [] # priority queue, we use negated support to order correctly
    extracted = 0
    returned = []

    supp_root, root_bits = trie._get_support_and_closure_bits_at_node(trie.root, 0)

    if root_bits > 0 and supp_root >= sigma:
        heapq.heappush(Q, (-supp_root, root_bits, len(trie.index_to_item) + 1))

    for j in range(1, len(trie.index_to_item) + 1):
        item_j_bit = 1 << (j - 1)
        if root_bits & item_j_bit: continue # item j already in X, so item can't extend X

        target = root_bits | item_j_bit
        supp_Y, Y_bits = trie._get_support_and_closure_bits_at_node(trie.root, target)
        # Y contains all items that always appear with X U item

        if supp_Y >= sigma:
            mask = (1 << (j - 1)) - 1 # Bits smaller than j
            if (Y_bits & mask) == (root_bits & mask):
                heapq.heappush(Q, (-supp_Y, Y_bits, j))

    while Q and -Q[0][0] >= sigma_prime: # Q[0] is the top of the queue
        supp_Y, Y_bits, i = heapq.heappop(Q)
        supp_Y = -supp_Y

        extracted += 1 # We extract the next closed itemset from the heap
        if extracted == K: 
            # If we have extracted enough items, we found the real minsup
            sigma_prime = supp_Y
        returned.append(trie.seq_to_transaction(Y_bits)) # We need to return the new itemset in FC (Y)

        if supp_Y > sigma:
            for j in range(i+1, len(trie.index_to_item)+1):
                item_j_bit = 1 << (j - 1)

                if Y_bits & item_j_bit: continue

                target = Y_bits | item_j_bit
                supp_X, X_bits = trie._get_support_and_closure_bits_at_node(trie.root, target)

                if supp_X >= sigma:
                    mask = (1 << (j - 1)) - 1
                    if (X_bits & mask) == (Y_bits & mask):
                        heapq.heappush(Q, (-supp_X, X_bits, j))

                    if extracted + len(Q) >= K:
                        # We can raise the lower bound
                        sigma = -heapq.nsmallest(K - extracted, Q)[-1][0]
                        Q = [e for e in Q if -e[0] >= sigma]
                        heapq.heapify(Q)

                        supp = Q[0][0]
                        while -supp < sigma:
                            heapq.heappop(Q)
                            supp = Q[0][0]
 
    return {"itemsets": returned}
