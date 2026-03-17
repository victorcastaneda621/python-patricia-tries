import data_structures.patricia_trie.transaction_to_bit_seq as tbs

## AUXILIARY FUNCTIONS ########################################################

def is_bit_i_of_seq_zero(seq, i):
        # Shift so rightmost bit is bit i and compare to 0b1.
        # If bit i was 0, 0 & 1 returns 0, if it was 1, 1 & 1 returns 1
        return ((seq >> i) & 1) == 0

def first_difference(seq1, seq2):
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

## NODE TYPES #################################################################

class Node():
    def __init__(self, subtrie_leaf_count: int, subtrie_or_mask: int):
        self.subtrie_leaf_count = subtrie_leaf_count
        self.subtrie_or_mask = subtrie_or_mask

class InternalNode(Node):
    def __init__(self, skip: int, left_child: Node, right_child: Node, subtrie_leaf_count: int, subtrie_or_mask: int):
        super().__init__(subtrie_leaf_count, subtrie_or_mask)
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
        super().__init__(value, key)
        self.key = key
        self.value = value # Amount of transactions equal to this one

## PATRICIA TRIE ##############################################################
class PatriciaTrieSeq():
    """PatriciaTrieSeq is a Patricia trie where transactions are transformed
    into bit sequences where bit j indicates if item j in the global order
    is in the transaction or not."""
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

    def get_value_from_bits(self, key: int):
        n = self._get_item_node(key)
        # If the key was in the trie, we found the corresponding node; 
        # otherwise it was not
        if n.key == key:
            return n.value
        else:
            return None
        
    def get_value_from_transaction(self, transaction: set):
        bit_seq = tbs.transactionToBitSequence(transaction, self.item_to_index)
        return self.get_value_from_bits(bit_seq)
    
    def insert(self, keys: list):
        # If we dont have an order (first insertion), we must obtain it
        if not self.index_to_item:
            self.index_to_item, self.item_to_index, support = tbs.find_item_order(keys)

        # Turn keys into bit sequences
        keys = tbs.transactionListToBitSequences(keys, self.item_to_index)

        # If the trie is empty, we need to add the first item as root
        if not self.root:
            self.root = LeafNode(keys[0], 1)
            keys = keys[1:]

        # At this point we know we already have at least one node
        # in the trie, and bit sequences as keys
        for key in keys:
            # General procedure
            n = self._get_item_node(key)

            if n.key != key:
                j = first_difference(n.key, key)
                parent = None
                current = self.root
                left_child = False

                while not isinstance(current, LeafNode) and current.skip < j:
                    current.subtrie_leaf_count += 1
                    current.subtrie_or_mask = current.subtrie_or_mask | key
                    parent = current
                    if is_bit_i_of_seq_zero(key, current.skip):
                        current = current.left_child
                        left_child = True
                    else:
                        current = current.right_child
                        left_child = False
                m = InternalNode(j, None, None, None, None)
                if not parent:
                    self.root = m
                else:
                    if left_child: # n was the left child
                        parent.set_left_child(m)
                    else:
                        parent.set_right_child(m)
                h = LeafNode(key, 1)
                if is_bit_i_of_seq_zero(key, j):
                    m.set_left_child(h)
                    m.set_right_child(current)
                else:
                    m.set_left_child(current)
                    m.set_right_child(h)
                m.subtrie_leaf_count = current.subtrie_leaf_count + h.subtrie_leaf_count
                m.subtrie_or_mask = current.subtrie_or_mask | h.subtrie_or_mask
            else: # Node already on the trie, we update the support
                current = self.root
                while current != n:
                    # Update the support of all ancestors
                    current.subtrie_leaf_count += 1
                    current.subtrie_or_mask |= key 
                    if is_bit_i_of_seq_zero(key, current.skip):
                        current = current.left_child
                    else:
                        current = current.right_child

                n.value += 1
                n.subtrie_leaf_count += 1
        return support
        
    def _print(self, n, i, pos):
        indentation = "    " * i
        if isinstance(n, LeafNode):
            print(indentation + pos + "├── (" + str(self.seq_to_transaction(n.key)) + " --> key: " + 
                  str(n.key) + ", support: " + str(n.value) + ")")
        else:
            print(indentation + pos + "├──" + "(skip: " + str(n.skip) + ")")
            self._print(n.get_left_child(), i+1, "L")
            self._print(n.get_right_child(), i+1, "R")
        
    def print(self):
        self._print(self.root, 0, "·")

    def seq_to_transaction(self, seq):
        return tbs.bitSequenceToTransaction(seq, self.index_to_item)
    
    def get_support_of_itemset(self, itemset: set):
        bit_seq = tbs.transactionToBitSequence(itemset, self.item_to_index)
        # We start at the root and follow edges until arriving at a leaf node
        return self._get_support_of_itemset_at_node(bit_seq, self.root)
    
    def get_support_of_itemset_as_bit_seq(self, bit_seq: int):
        # We start at the root and follow edges until arriving at a leaf node
        return self._get_support_of_itemset_at_node(bit_seq, self.root)
    
    def _get_support_of_itemset_at_node(self, bit_seq, node):
        and_result = node.subtrie_or_mask & bit_seq
        if and_result == bit_seq:
            # i.e. the node's OR mask has 1s at least in the same places 
            # as the bit_seq
            if isinstance(node, LeafNode): 
                # We arrived at a key that contains 1s in every required position
                return node.value
            else: 
                # we continue exploring children
                if not is_bit_i_of_seq_zero(bit_seq, node.skip):
                    # If the target bit_seq requires a 1 at node.skip, we only explore the 
                    # right child. The left child is a dead end (path where that bit is 0).
                    return self._get_support_of_itemset_at_node(bit_seq, node.right_child)
                else:
                    # The target doesn't care about this bit, so explore both branches
                    left_supp = self._get_support_of_itemset_at_node(bit_seq, node.left_child)
                    right_supp = self._get_support_of_itemset_at_node(bit_seq, node.right_child)
                    return left_supp + right_supp
        else:
            # We should stop exploring this subtrie
            return 0
        
    def count_nodes(self):
        return self._count_nodes(self.root)
    
    def _count_nodes(self, node):
        if isinstance(node, LeafNode):
            return 1
        else: 
            left_count = self._count_nodes(node.left_child)
            right_count = self._count_nodes(node.right_child)
            return left_count + right_count

## PatriciaTrieSeq ############################################################
# example = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}] 
# has supports [Atenas:1, Roma:2, Oslo:3], so it becomes [0b111, 0b011, 0b001]. 
# The trie is:
# Sequence values:  [7, 3, 1]
#·├──(skip: 1)
#    L├──1 (value: t3)
#    R├──(skip: 2)
#        L├──3 (value: t2)
#        R├──7 (value: t1)