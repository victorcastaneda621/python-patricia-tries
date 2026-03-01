import transaction_to_bit_seq as tbs

## AUXILIARY FUNCTIONS ########################################################

def is_bit_i_of_seq_zero(seq, i):
        # Shift so rightmost bit is bit i and compare to 0b1.
        # If bit i was 0, 0 & 1 returns 0, if it was 1, 1 & 1 returns 1
        return ((seq >> i) & 1) == 0

def first_difference(seq1, seq2):
        xor = seq1 ^ seq2 # seq1 XOR seq2
        # Now the leftmost 1 is the first 
        if xor == 0:
            return None # There will be no differences
        
        i = 0
        while xor > 0:
            if xor & 1 == 1: # Then XOR returned 1 for the first time at i 
                return i
            xor = xor >> 1 # Shift to the right (0b1011 >> 1 = 0b(0)101)
            i += 1
        return None

## NODE TYPES #################################################################

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

    def get_left_child(self):
        return self.left_child

    def get_right_child(self):
        return self.right_child
        
class LeafNode(Node):
    def __init__(self, key: int, value):
        super().__init__()
        self.key = key
        self.value = value

## PATRICIA TRIE ##############################################################

class PatriciaTrie():
    def __init__(self):
        self.root = None
        self.item_to_index = None
        self.index_to_item = None
    
    def _get_item_node(self, key: int):
        # If the trie is empty, the key is not in the trie
        if not self.root:
            return None
        
        # We start at the root and follow edges until arriving at a leaf node
        n = self.root
        while not isinstance(n, LeafNode):
            # Shift the bit we need to compare to the right, 
            # then compare it with 0...01
            if is_bit_i_of_seq_zero(key, n.skip):
                n = n.left_child
            else:
                n = n.right_child
        return n # If the key was not in the trie, we still return some node

    def get_from_bits(self, key: int):
        n = self._get_item_node(key)
        # If the key was in the trie, we found the corresponding node; 
        # otherwise it was not
        if n.key == key:
            return n.value
        else:
            return None
        
    def get_from_transaction(self, transaction: set):
        bit_seq = tbs.transactionToBitSequence(transaction, self.item_to_index)
        return self.get_from_bits(bit_seq)
    
    def insert(self, items: list):
        # Separate keys and values
        keys, values = zip(*items)

        # If we dont have an order (first insertion), we must obtain it
        if not self.index_to_item:
            self.index_to_item, self.item_to_index = tbs.find_item_order(keys)

        # Turn keys into bit sequences
        keys = tbs.transactionListToBitSequences(keys, self.item_to_index)

        # If the trie is empty, we need to add the first item as root
        if not self.root:
            self.root = LeafNode(keys[0], values[0])
            keys = keys[1:]
            values = values[1:]

        # At this point we know we already have at least one node
        # in the trie, and bit sequences as keys
        items = zip(keys, values)
        for key,value in items:
            # General procedure
            n = self._get_item_node(key)
            if not n.key == key:
                j = first_difference(n.key, key)
                parent = None
                n = self.root
                left_or_right = 0
                while not isinstance(n, LeafNode) and n.skip < j:
                    parent = n
                    if is_bit_i_of_seq_zero(key, n.skip):
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
                if is_bit_i_of_seq_zero(key, j):
                    m.set_left_child(h)
                    m.set_right_child(n)
                else:
                    m.set_left_child(n)
                    m.set_right_child(h)
            else: # Node already on the trie, we update the value
                n.value += value
        
    def _print(self, n, i, pos):
        indentation = "    " * i
        if isinstance(n, LeafNode):
            print(indentation + pos + "├──" + str(n.key) + " (value: " + str(n.value) + ")")
        else:
            print(indentation + pos + "├──" + "(skip: " + str(n.skip) + ")")
            self._print(n.get_left_child(), i+1, "L")
            self._print(n.get_right_child(), i+1, "R")
        
    def print(self):
        self._print(self.root, 0, "·")

def testing_bit_seq(ts):
    #print("Transactions: ", ts)
    index_to_item, item_to_index = tbs.find_item_order([k for k,_ in ts])
    #print(item_to_index)
    seqs = tbs.transactionListToBitSequences([k for k,_ in ts], item_to_index)
    print("Sequence values: ", seqs)
    trie = PatriciaTrie()
    trie.insert(ts)
    trie.print()
    #trie.insert([{"Praga"}]) # Not allowed for now
    print(trie.get_from_transaction({"Atenas", "Oslo"}))

# example = [({"Atenas", "Oslo", "Roma"}, "t1"), ({"Atenas", "Oslo"}, "t2"),
# ({"Oslo"}, "t3")] has supports [Atenas:1, Roma:2, Oslo:3], so it becomes 
# [0b111, 0b011, 0b001]. The the trie is:
# Sequence values:  [7, 3, 1]
#·├──(skip: 1)
#    L├──1 (value: t3)
#    R├──(skip: 2)
#        L├──3 (value: t2)
#        R├──7 (value: t1)
#example = [({"Atenas", "Oslo", "Roma"}, "t1"), ({"Atenas", "Oslo"}, "t2"), ({"Oslo"}, "t3")]
#testing_bit_seq(example)