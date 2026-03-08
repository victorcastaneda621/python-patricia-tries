import time
import transaction_to_bit_seq as tbs
import patricia_trie as pt  # your implementation
from collections import Counter

# Try to import the library trie
import patricia

# Load dataset (mushroom)
from ucimlrepo import fetch_ucirepo

mushroom = fetch_ucirepo(id=73)
X = mushroom.data.features

def row_to_transaction(row):
    transaction = set()
    for col, value in row.items():
        transaction.add(f"{col}={value}")
    return transaction

transactions = [row_to_transaction(row) for _, row in X.iterrows()]


def bench_your_trie():
    """Benchmark your Patricia trie using batch insertion."""
    start = time.time()
    trie = pt.PatriciaTrie()

    # Prepare keys and values in batch
    keys = transactions
    values = [1] * len(transactions)  # initial support = 1

    items = list(zip(keys, values))
    trie.insert(items)  # insert all at once
    insert_time = time.time() - start

    # Test lookup
    lookup_keys = transactions[:100]
    start = time.time()
    for t in lookup_keys:
        bit = tbs.transactionToBitSequence(t, trie.item_to_index)
        _ = trie.get_value_from_bits(bit)
    lookup_time = time.time() - start

    return insert_time, lookup_time


def bench_lib_trie():
    trie = patricia.trie()
    start_insert = time.time()
    for t in transactions:
        key = ",".join(sorted(t))
        trie[key] = trie[key] + 1 if key in trie else 1
    end_insert = time.time()

    # Lookup some random keys
    sample_keys = transactions[:100]
    start_lookup = time.time()
    supports = []
    for t in sample_keys:
        key = ",".join(sorted(t))
        supports.append(trie[key] if key in trie else 0)
    end_lookup = time.time()

    return end_insert - start_insert, end_lookup - start_lookup, supports

if __name__ == "__main__":
    print("Benchmarking your Patricia trie…")
    your_insert, your_lookup = bench_your_trie()
    print(f"Your trie:   insert={your_insert:.4f}s  lookup={your_lookup:.4f}s")

    if patricia:
        print("Benchmarking patricia-trie library…")
        lib_insert, lib_lookup, lib_supports = bench_lib_trie()
        print(f"lib trie:    insert={lib_insert:.4f}s  lookup={lib_lookup:.4f}s")
    else:
        print("Library trie not installed; skipping.")