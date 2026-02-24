from ucimlrepo import fetch_ucirepo 
import patricia_interface, patricia
  
# fetch dataset 
mushroom = fetch_ucirepo(id=73)
X = mushroom.data.features

def row_to_transaction(row):
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

transactions = [row_to_transaction(row) for _, row in X.iterrows()]
support_dict = patricia_interface.count_support(transactions)
global_order, reverse_order = patricia_interface.generate_global_order_descending_support(support_dict)
sequence_list = patricia_interface.transactionListToSequences(transactions, global_order)

trie = patricia.trie()
for seq in sequence_list:
    trie[seq] = True

prefix = "11111"
print(len(trie.keys(prefix)))
for seq in trie.keys():
    if seq.startswith(prefix):
        transaction = patricia_interface.prefixBitSequenceToTransaction(seq, reverse_order)
        print(transaction)