from collections import Counter
import math

## patricia_enc (sequences where each item is represented #####################
## by a unique bit sequence, which are made as short as possible) #############
def find_item_order_and_codification(transaction_list: list):
    # Count support
    support = Counter()
    for t in transaction_list:
        support.update(t)

    # Global item order
    item_order = sorted(support.keys(), key=lambda x: (-support[x], x))
    # Number of total bits per item needed
    bits_per_item = math.ceil(math.log(len(item_order), 2))

    # Build the item econdings
    item_to_encoding = {}
    encoding_to_item = {}
    for i, item in enumerate(item_order):
        item_to_encoding[item] = i
        encoding_to_item[i] = item
    return encoding_to_item, item_to_encoding, bits_per_item, support

def transactionToEncoding(t: list, item_to_encoding: dict, bits_per_item: int):
    t_encoded = 0
    sorted_t = sorted(t, key=lambda x: item_to_encoding[x])
    for i in range(0,len(sorted_t)):
        enc_to_add = item_to_encoding[sorted_t[i]]
        t_encoded = t_encoded + (enc_to_add << bits_per_item*i)
    return t_encoded

def transactionListToEncoding(transaction_list: list, item_to_encoding: dict, bits_per_item: int):
    return [transactionToEncoding(t, item_to_encoding, bits_per_item) for t in transaction_list]

def encodingToTransaction(encoding: int, encoding_to_item: dict, bits_per_item: int):
    t = []
    while encoding > 0:
        