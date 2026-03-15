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
        if not itemset: # Empty itemset case
            return self.root.support if self.root else 0
        # We start at the root having checked 0 items of the itemset
        return self._get_support_of_itemset_at_node(itemset, self.root, 0, order)
    
    def _get_support_of_itemset_at_node(self, itemset, node, j, order):
        # Check the current node's prefix
        for i in range(0, len(node.prefix)):
            # Stop if we have already checked every item from the itemset
            if j == len(itemset): 
                return node.support
            elif node.prefix[i] == itemset[j]:
                j += 1 # We have to check the next item in the itemset
            elif self._compare_to(node.prefix[i], itemset[j], order) == 1: 
                # Entering here means that this node is missing some items of the itemset
                return 0
        # Stop if we have already checked every item from the itemset
            if j == len(itemset): 
                return node.support
        
        # Now, if we didn't return, we must continue checking this node's children
        result = 0
        if isinstance(node, LeafNode):
            # Then it has no children, so we return while having not
            # found the full itemset
            return 0
        elif isinstance(node, SingleChildNode):
            # We check the child if it looks promising
            if self._compare_to(node.child.prefix[0], itemset[j], order) != 1:
                # It is promising, so we explore it
                result += self._get_support_of_itemset_at_node(
                    itemset, node.child, j, order
                    )
        else: # It is a MultiChildNode
            # We check any of its children if it looks promising
            for child_key in node.children.keys():
                if self._compare_to(child_key, itemset[j], order) != 1:
                    result += self._get_support_of_itemset_at_node(
                        itemset, node.children[child_key], j, order
                        )
        return result
        
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
# Using the order makes sure that if we see item1 and item4 and item5 as its children,
# item2 and item3 cannot be anywhere in the subtree
"""example = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}, {"Praga", "Oslo"}, 
           {"Londres", "Kyiv", "Tallin"}, {"Londres", "Kyiv", "Dublin"}, {"Atenas", "Kyiv"}]
tree = RadixTree()
transactions, support, order = radix_tree_count_sort(example)
print("order: ", order)
tree.insert(transactions)
tree.print()
print('support(["Atenas"]): ' + str(tree.get_support_of_itemset(["Atenas"], order)))
print('support(["Oslo"]): ' + str(tree.get_support_of_itemset(["Oslo"], order)))
print('support(["Atenas", "Oslo"]): ' + str(tree.get_support_of_itemset(["Oslo", "Atenas"], order)))
print('support(["Atenas", "Tallin"]): ' + str(tree.get_support_of_itemset(["Atenas", "Tallin"], order)))
print('support(["Oslo", "Londres"]): ' + str(tree.get_support_of_itemset(["Oslo", "Londres"], order)))
print('support(["Oslo", "Roma"]): ' + str(tree.get_support_of_itemset(["Oslo", "Roma"], order)))
print('support(["Kyiv"]): ' + str(tree.get_support_of_itemset(["Kyiv"], order)))
print("\n--- Extended Testing ---")
# Case A: Partial match in the middle of a multi-item prefix
# Searching for "Londres" when the node is ['Kyiv', 'Londres']
print('support(["Londres"]): ' + str(tree.get_support_of_itemset(["Londres"], order)))
# Case B: The "Empty" Itemset (Should theoretically be the total number of transactions)
print('support([]): ' + str(tree.get_support_of_itemset([], order)))
# Case C: Itemset that doesn't exist but its items do (in the wrong order or combo)
# Oslo and Dublin both exist, but never together.
print('support(["Oslo", "Dublin"]): ' + str(tree.get_support_of_itemset(["Oslo", "Dublin"], order)))
# Case D: Deeply nested match
# Checking if it finds "Roma" even though it's at the very tip of a long branch
print('support(["Roma"]): ' + str(tree.get_support_of_itemset(["Roma"], order)))
# Case E: Non-existent item entirely (doesnt handle it, but it should never come up)"""