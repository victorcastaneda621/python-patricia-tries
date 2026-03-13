
class Node():
    def __init__(self, prefix: list, value: int, is_terminal: bool):
        self.prefix = prefix
        self.value = value
        self.is_terminal = is_terminal

class LeafNode(Node):
    def __init__(self, prefix: list, value: int):
        super().__init__(prefix, value, True)

class SingleChildNode(Node):
    def __init__(self, prefix: list, value: int, is_terminal: bool, child: Node = None):
        super().__init__(prefix, value, is_terminal)
        self.child = child

class MultiChildNode(Node):
    def __init__(self, prefix: list, value: int, is_terminal: bool, children: dict = None):
        super().__init__(prefix, value, is_terminal)
        self.children = children if children else {}
    
    def add_child(self, key, child: Node):
        self.children[key] = child
    
    def remove_child(self, child):
        pass #TODO

## RADIX TREE ##############################################################

class RadixTree():
    def __init__(self):
        self.root = None
    
    def _get_common_prefix_length(self, prefix1, prefix2):
        smaller_prefix_len = min(len(prefix1), len(prefix2))
        for i in range(smaller_prefix_len):
            if prefix1[i] != prefix2[i]:
                return i
        # The last possible value for i was smaller_prefix_len - 1
        return smaller_prefix_len
    
    def _replace_child(self, parent, new_node):
        if parent is None:
            self.root = new_node
        elif isinstance(parent, SingleChildNode):
            parent.child = new_node
        else:
            parent.children[new_node.prefix[0]] = new_node
            
    def insert(self, keys: list):
        # Turn sets into lists (giving the items an order)
        keys = [sorted(key) for key in keys]

        # If the tree is empty, we need to add the first item as root
        if not self.root:
            self.root = LeafNode(keys[0], 1)
            keys = keys[1:]

        # At this point we know we already have at least one node in the tree
        for key in keys:
            # General procedure
            n = self.root
            n_parent = None
            finished_adding_current_key = False
            while not finished_adding_current_key:
                if key == n.prefix:
                    n.value += 1
                    finished_adding_current_key = True
                else:  
                    i = self._get_common_prefix_length(n.prefix, key)
                    # Right now i can be the first difference, 
                    # len(key) or len(n.prefix)
                    if i == len(key):
                        # len(key) < len(n.prefix) AND key = n.prefix[:i]
                        m = SingleChildNode(n.prefix[:i], n.value, True, n)
                        n.prefix = n.prefix[i:]
                        self._replace_child(n_parent, m)

                        finished_adding_current_key = True
                    elif i == len(n.prefix):
                        # len(key) > len(n.prefix) AND key[:i] = n.prefix
                        if isinstance(n, LeafNode):
                            m = LeafNode(key[i:], 1)
                            new_n = SingleChildNode(n.prefix, n.value, n.is_terminal, m)
                            self._replace_child(n_parent, new_n)

                            finished_adding_current_key = True
                        elif isinstance(n, SingleChildNode):
                            n_parent = n
                            n = n.child
                            continue
                        elif isinstance(n, MultiChildNode):
                            if key[i] in n.children:
                                n_parent = n
                                n = n.children[key[i]]
                                continue
                            else:
                                m = LeafNode(key[i:], 1)
                                n.children[key[i]] = m
                                finished_adding_current_key = True
                    else:
                        # The first difference was found before 
                        # the end of key or n.prefix
                        pass
        
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

# example = [({"Atenas", "Oslo", "Roma"}, "t1"), ({"Atenas", "Oslo"}, "t2"),
# ({"Oslo"}, "t3")] has supports [Atenas:1, Roma:2, Oslo:3], so it becomes 
# [0b111, 0b011, 0b001]. The the trie is:
# Sequence values:  [7, 3, 1]
#·├──(skip: 1)
#    L├──1 (value: t3)
#    R├──(skip: 2)
#        L├──3 (value: t2)
#        R├──7 (value: t1)
example = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}]
tree = RadixTree()
tree.insert(example)