
import patricia

class PatriciaTrie(patricia.trie):

    def __init__(self, transactions):
        super().__init__(transactions)


def TransactionToBitSequence(transaction: set, global_order: dict):
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
        if item in global_order:
            pos = global_order[item]
            seq[pos] = "1"
        else:
            raise Exception(f"TransactionToBitSequence: Item {item} of transaction " +
            "not found in global order")
    return ''.join(seq)
print(TransactionToBitSequence({1,4,6}, {1:0,2:1,3:2,4:3,5:4}))

def TransactionListToSequences(transactions: list, support: dict):
    """
    Returns a list of bit sequences obtained from each transaction in the list.
    
    :param transactions: List of transactions
    :param support: Supports of the items (determines global order) {item:support}
    """
    # Find out global order
    global_order = {}
    i = 0
    items = sorted(support.items(), lambda x,y: y)
    while items:
        max = items
        supp.remove(max)
    support.
    # Generate the list of bit sequences
    seqs = []