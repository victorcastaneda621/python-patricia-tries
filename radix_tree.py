from general_utils import radix_tree_count_sort

class Node():
    def __init__(self, prefix: list, support: int, is_terminal: bool):
        self.prefix = prefix
        self.support = support
        self.is_terminal = is_terminal

class LeafNode(Node):
    def __init__(self, prefix: list, support: int):
        super().__init__(prefix, support, True)

class SingleChildNode(Node):
    def __init__(self, prefix: list, support: int, is_terminal: bool, child: Node = None):
        super().__init__(prefix, support, is_terminal)
        self.child = child

class MultiChildNode(Node):
    def __init__(self, prefix: list, support: int, is_terminal: bool, children: dict = None):
        super().__init__(prefix, support, is_terminal)
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
        # keys = [sorted(key) for key in keys]

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
                    n.support += 1
                    finished_adding_current_key = True
                else:  
                    i = self._get_common_prefix_length(n.prefix, key)
                    # Right now i can be the first difference, 
                    # len(key) or len(n.prefix)
                    if i == len(key):
                        # len(key) < len(n.prefix) AND key = n.prefix[:i]
                        m = SingleChildNode(n.prefix[:i], n.support + 1, True, n)
                        n.prefix = n.prefix[i:]
                        self._replace_child(n_parent, m)

                        finished_adding_current_key = True
                    elif i == len(n.prefix):
                        # len(key) > len(n.prefix) AND key[:i] = n.prefix
                        n.support += 1
                        if isinstance(n, LeafNode):
                            m = LeafNode(key[i:], 1)
                            new_n = SingleChildNode(n.prefix, n.support, True, m)
                            self._replace_child(n_parent, new_n)

                            finished_adding_current_key = True
                        elif isinstance(n, SingleChildNode):
                            if n.child.prefix[0] == key[i]:
                                n_parent = n
                                n = n.child
                                continue
                            else:
                                m = MultiChildNode(n.prefix, n.support, n.is_terminal)
                                m.children[n.child.prefix[0]] = n.child
                                m.children[key[i]] = LeafNode(key[i:], 1)
                                self._replace_child(n_parent, m)
                                finished_adding_current_key = True
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
                        m = MultiChildNode(n.prefix[:i], n.support + 1, False)
                        m.children[n.prefix[i]] = n
                        m.children[key[i]] = LeafNode(key[i:], 1)
                        self._replace_child(n_parent, m)
                        n.prefix = n.prefix[i:]
                        finished_adding_current_key = True

    def _compare_to(self, key1, key2, order):
        if order[key1] < order[key2]:
            return -1
        elif order[key1] > order[key2]:
            return 1
        else:
            return 0

    def get_support_of_itemset(self, itemset: list, order):
        # We start at the root and follow edges until arriving at a leaf node
        return self._get_support_of_itemset_at_node(itemset, self.root, 0, order)
    
    def _get_support_of_itemset_at_node(self, itemset, node, i, order):
        support = 0
        if i == len(itemset): 
            # We should stop now
            return node.support if node.is_terminal else 0
        elif isinstance(node, LeafNode): 
            # This node might contain the itemset
            j = 0
            while i+j < len(itemset) and j < len(node.prefix) and node.prefix[j] == itemset[i+j]:
                j += 1
            if j == len(itemset) - i:
                return node.support
            else:
                return 0
        elif isinstance(node, SingleChildNode): 
            # We explore the child if it looks promising
            if self._compare_to(node.child.prefix[0], itemset[i], order) != -1:
                support += self._get_support_of_itemset_at_node(
                    itemset, node.child, i+1, order)
        else:
            for child_key, child in node.children.items():
            # We explore those children that look promising
                cmp = self._compare_to(child_key, itemset[i], order)
                if cmp == -1: 
                    # Item i could still appear later, 
                    # but not through this child
                    continue
                elif cmp == 1: 
                    # Due to the ordering, we know the subtree 
                    # cannot contain item i, so we prune it
                    support += self._get_support_of_itemset_at_node(
                        itemset, child, i, order)
                else:
                    # We found item i of the itemset
                    support += self._get_support_of_itemset_at_node(
                        itemset, child, i+1, order)
        return support

        
    def _print(self, n, i, item):
        indentation = "       " * i
        if isinstance(n, LeafNode):
            print(indentation + item + "├── (" + "--> " +
                  str(n.prefix) + ", support: " + str(n.support) + ")")
        elif isinstance(n, SingleChildNode):
            print(indentation + item + "├── (" + "--> " +
                  str(n.prefix) + ", support: " + str(n.support) + ")")
            label = n.child.prefix[0] if n.child.prefix else "[]"
            self._print(n.child, i+1, label)
        else:
            print(indentation + item + "├── (" + "--> " +
                  str(n.prefix) + ", support: " + str(n.support) + ")")
            for item, child in n.children.items():
                self._print(child, i+1, item)
        
    def print(self):
        self._print(self.root, 0, str(self.root.prefix))

# example = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}]
#
#·├── (--> [], support: 3)
#       Atenas├── (--> ['Atenas'], support: 2)   
#              Roma├── (--> ['Roma'], support: 1)
example = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}, {"Praga", "Oslo"}, 
           {"Londres", "Kyiv", "Tallin"}, {"Londres", "Kyiv", "Dublin"}, {"Atenas", "Kyiv"}]
tree = RadixTree()
transactions, support, order = radix_tree_count_sort(example)
tree.insert(transactions)
tree.print()
print("support: " + str(tree.get_support_of_itemset(["Atenas"], order)))