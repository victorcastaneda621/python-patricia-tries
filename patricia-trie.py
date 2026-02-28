from collections import Counter

def find_item_order(transaction_list: list):
    # Build the universe of items
    universe = [item for t in transaction_list for item in t]
    # Count support ()
    support = Counter(universe)
    # Build the order list and order dictionary
    # index -> item
    index_to_item = [item for item, _ in support.most_common()]
    # item -> index
    item_to_index = {item:i for i, item in enumerate(index_to_item)}
    return index_to_item, item_to_index

def transactionToBitSequence(t: set, item_to_index: dict):
    bit_seq = 0
    for item in t:
        i = item_to_index[item]
        # bit_seq = bit_seq OR (1 shifted i places to the left)
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

class Node():
    pass

class InternalNode(Node):
    def __init__(self, skip: int, left_child: Node, right_child: Node):
        super().__init__()
        self.skip = skip
        self.left_child = left_child
        self.right_child = right_child

    def set_left_child(self, left_child):
        self.left_child = left_child

    def set_right_child(self, right_child):
        self.right_child = right_child
        
class LeafNode(Node):
    def __init__(self, key: int, value):
        super().__init__()
        self.key = key
        self.value = value

class PatriciaTrie():
    def __init__(self):
        self.root = None
        self.item_to_index = None
        self.index_to_item = None

    def _is_bit_i_of_seq_zero(self, seq, i):
        # Shift so rightmost bit is bit i and compare to 0b1
        return ((seq >> i) & 1) == 0
    
    def _get_item_node(self, key: int):
        # If the trie is empty, the key is not in the trie
        if not self.root:
            return None
        
        # We start at the root and follow edges until arriving at a leaf node
        n = self.root
        i = 0
        while not isinstance(n, LeafNode):
            i += n.skip
            # Shift the bit we need to compare to the right, 
            # then compare it with 0...01
            if self._is_bit_i_of_seq_zero(key, i):
                n = n.left_child
            else:
                n = n.right_child
        return n # If the key was not in the trie, we still return some node

    def _first_difference(self, seq1, seq2):
        xor = seq1 ^ seq2 # seq1 XOR seq2
        # Now the leftmost 1 is the first difference
        if xor == 0:
            return None # There will be no differences
        
        i = 0
        while xor > 0:
            if xor & 1 == 1: # Then XOR returned 1 for the first time at i 
                return i
            xor = xor >> 1 # Shift to the right (0b1011 >> 1 = 0b(0)101)
            i += 1
        return None
    
    def insert(self, items: list):
        keys, values = zip(*items)
        if not self.index_to_item: # First insertion, we need the orders
            self.index_to_item, self.item_to_index = find_item_order(keys)
        keys = transactionListToBitSequences(keys, self.item_to_index)
        items = list(zip(keys, values))
        if not self.root: # If the trie is empty, we add the first item as root
            self.root = LeafNode(keys[0], values[0])

        # At this point we already have at least one node in the trie, and bit sequences as keys
        for key,value in items:
            n = self._get_item_node(key)

            if isinstance(n, LeafNode): # If we only have one node, it wont have a skip value
                j = self._first_difference(n.key, key) ---# This can return None and that is a problem, function might work badly cause it should not return None in this case
                m = InternalNode(j, None, None)
                h = LeafNode(key, value)
                if self._is_bit_i_of_seq_zero(key, j):
                    m.set_left_child(h)
                    m.set_right_child(n)
                else:
                    m.set_left_child(n)
                    m.set_right_child(h)
                self.root = m
                continue

            # General procedure (trie with 2 keys or more already)
            if not n == key:
                j = self._first_difference(n.key, key)
                if j is None:
                    # The key already exists in the trie, so we skip insertion
                    continue
                parent = None
                i = n.skip
                left_or_right = 0
                while i < j and not isinstance(n, LeafNode):
                    i = n.skip
                    parent = n
                    if self._is_bit_i_of_seq_zero(key, i):
                        n = n.left_child
                        left_or_right = 0
                    else:
                        n = n.right_child
                        left_or_right = 1
                m = InternalNode(j, None, None)
                if not parent:
                    self.root = m
                else:
                    if left_or_right == 0: # n was the left child
                        parent.set_left_child(m)
                    else:
                        parent.set_right_child(m)
                h = LeafNode(key, value)
                if self._is_bit_i_of_seq_zero(key, j):
                    m.set_left_child(h)
                    m.set_right_child(n)
                else:
                    m.set_left_child(n)
                    m.set_right_child(h)

    def get(self, key: int):
        n = self._get_item_node(key)
        # If the key was in the trie, we found the corresponding node; 
        # otherwise it was not
        if n.key == key:
            return n.value
        else:
            return None

def testing_bit_seq(ts):
    #print("Transactions: ", ts)
    #index_to_item, item_to_index = find_item_order(ts)
    #print(item_to_index)
    #seqs = transactionListToBitSequences(ts, item_to_index)
    #print("Sequence values: ", seqs)
    trie = PatriciaTrie()
    trie.insert(ts)
    print(trie.get(0b01111))

example = [({"Atenas", "Oslo", "Roma", "Vienna"}, "t1"), ({"Atenas", "Oslo", "Roma", "Praga"}, "t2"), ({"Oslo", "Roma", "Vienna"}, "t3"), ({"Oslo"}, "t4")]
testing_bit_seq(example)