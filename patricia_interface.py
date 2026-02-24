
def transactionToBitSequence(transaction: set, global_order: dict):
    """
    Transforms a transaction t1 = {i1, i2, ..., in} into a bit sequence, where each
    bit determines whether the item in position j of the global order is included in 
    the transaction or not.
    
    :param transaction: Transaction to transform into a bit sequence.
    :param global_order: Global order of the items that can appear in a transaction.
    If an item of the transaction is not present here, an error will be returned.
    If it is present, iit will be stored (key:value) as item:pos.
    """
    seq = ["0"] * len(global_order)
    for item in transaction:
        pos = global_order[item]
        seq[pos] = "1"
    return ''.join(seq)

def prefixBitSequenceToTransaction(bit_prefix: str, reverse_order: dict):
    t = set()
    i = 0
    for bit in bit_prefix:
        if bit == "1":
            t.add(reverse_order[i])
        i += 1
    return t

def transactionListToSequences(transactions: list, global_order: dict):
    """
    Returns a list of bit sequences obtained from each transaction in the list.
    
    :param transactions: List of transactions
    :param support: Supports of the items (determines global order) {item:support}
    """
    seqs = []
    for t in transactions:
        seqs.append(transactionToBitSequence(t, global_order))
    return seqs


def count_support(transactions: list):
    support = {}
    for t in transactions:
        for item in t:
            if item in support:
                support[item] += 1
            else:
                support[item] = 1
    return support

def generate_global_order_descending_support(support):
    global_order = {}
    i = 0
    items = sorted(support.items(), key=lambda x: x[1], reverse=True)
    for item,_ in items:
        global_order[item] = i
        i += 1
    reverse_order = {pos: item for item, pos in global_order.items()}
    return global_order, reverse_order