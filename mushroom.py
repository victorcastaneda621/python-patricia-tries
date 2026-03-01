from ucimlrepo import fetch_ucirepo 
import patricia_trie as pt
  
# fetch dataset 
mushroom = fetch_ucirepo(id=73)
X = mushroom.data.features

def row_to_transaction(row):
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

#transactions = [row_to_transaction(row) for _, row in X.iterrows()]
transactions = [{"Atenas", "Oslo", "Roma", "Vienna"}, {"Oslo"}, {"Oslo", "Roma", "Vienna"}, {"Oslo"}]
transactions_supp = [(t, 1) for t in transactions]

trie = pt.PatriciaTrie()
trie.insert(transactions_supp)
trie.print()

from collections import Counter
import transaction_to_bit_seq as tbs

# Convert dataset rows to transactions (sets of "col=value")
transactions = [row_to_transaction(row) for _, row in X.iterrows()]

# Count how many duplicates there are
bit_seqs = [tbs.transactionToBitSequence(t, tbs.find_item_order([t])[1]) for t in transactions]

counts = Counter(bit_seqs)
# Print all transactions that appear more than once
duplicates = {seq: count for seq, count in counts.items() if count > 1}
print("Transactions with support > 1:", duplicates)