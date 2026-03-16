## patricia_trie_short (sequences where each item is represented ##############
## by a unique bit sequence, which are made as short as possible) #############
def find_item_order_and_codification(transaction_list: list):
    # Build the universe of items
    universe = [item for t in transaction_list for item in t]
    # Count support
    support = Counter(universe)
    # Build the order list and order dictionary
    # index -> item
    index_to_item = [item for item, _ in support.most_common()]
    # item -> index
    item_to_index = {item:i for i, item in enumerate(index_to_item)}
    return seq_to_item, item_to_seq, item_order, support

def transactionToEncoding(t: set, item_to_index: dict):