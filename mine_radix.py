from radix_tree import RadixTree
import transaction_to_bit_seq as tbs
from ucimlrepo import fetch_ucirepo
#from patrix import RadixTree

### Small example dataset #################################################################
#transactions = [{"Atenas", "Oslo", "Roma", "Viena"}, {"Oslo"}, 
#                {"Oslo", "Roma", "Viena"}, {"Oslo"}, {"Londres", "Madrid"}, 
#                {"Londres", "Madrid", "Oslo"}]
### Fetch mushroom dataset ################################################################# 
mushroom = fetch_ucirepo(id=73)
X = mushroom.data.features
### Fetch connect-4 dataset ################################################################# 
#connect_4 = fetch_ucirepo(id=26)
#X = connect_4.data.features

def row_to_transaction(row):
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

transactions = [row_to_transaction(row) for _, row in X.iterrows()]

index_to_item, item_to_index = tbs.find_item_order(transactions)
bit_seqs = tbs.transactionListToBitSequences(transactions, item_to_index)
r = RadixTree()

for t in bit_seqs:
    r.insert_node(t, 1)

import sys

def total_size(obj, seen=None):
    """Recursively find the memory size of an object including its contents."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum(total_size(v, seen) + total_size(k, seen) for k, v in obj.items())
    elif hasattr(obj, '__dict__'):
        size += total_size(vars(obj), seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        size += sum(total_size(i, seen) for i in obj)
    return size
print("Size of radix-tree: ", total_size(r))
