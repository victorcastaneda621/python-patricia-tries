from collections import Counter

## patricia_trie_long (sequences where each bit represents ####################
## whether item j is or isn't in the transaction, producing long sequences) ###

def find_item_order(transaction_list: list):
    # Build the universe of items
    universe = [item for t in transaction_list for item in t]
    # Count support
    support = Counter(universe)
    # Build the order list and order dictionary
    # index -> item
    index_to_item = [item for item, _ in support.most_common()]
    # item -> index
    item_to_index = {item:i for i, item in enumerate(index_to_item)}
    return index_to_item, item_to_index, support

def transactionToBitSequence(t: set, item_to_index: dict):
    bit_seq = 0
    for item in t:
        i = item_to_index[item]
        # bit_seq = bit_seq OR (1 shifted i places to the left) 
        # i.e. put a 1 on position i of the bit sequence
        bit_seq = bit_seq | (1 << i)
    return bit_seq

def transactionListToBitSequences(transaction_list: list, item_to_index: dict):
    seqs = []
    for t in transaction_list:
        seqs.append(transactionToBitSequence(t, item_to_index))
    return seqs

def bitSequenceToTransaction(seq: int, index_to_item: dict):
    t = set()
    for i in range(0, len(index_to_item)):
        shifted = seq >> i # Shift so bit i is the rightmost
        if shifted == 0:
            break # There are no more elements to add, no need to check
        elif shifted & 1: # Check if the rightmost bit is 1
            t.add(index_to_item[i])
    return t

def bitSequenceListToTransaction(seqs: list, index_to_item: list):
    transactions = []
    for seq in seqs:
        transactions.append(bitSequenceToTransaction(seq, index_to_item))
    return transactions
