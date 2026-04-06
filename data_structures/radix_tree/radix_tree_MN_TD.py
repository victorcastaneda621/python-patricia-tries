from radix_tree_utils import Node, RadixTree

class LeafNode(Node):
    __slots__ = ['node_type']
    def __init__(self, prefix: list, count: int):
        super().__init__(prefix, count, True)
        self.node_type = 0

class SingleChildNode(Node):
    __slots__ = ['child', 'node_type']
    def __init__(self, prefix: list, count: int, is_terminal: bool, child: Node = None):
        super().__init__(prefix, count, is_terminal)
        self.child = child
        self.node_type = 1

class MultiChildNode(Node):
    __slots__ = ['children', 'node_type']
    def __init__(self, prefix: list, count: int, is_terminal: bool, children: dict = None):
        super().__init__(prefix, count, is_terminal)
        self.children = children if children else {}
        self.node_type = 2

class RadixTree_MN_TD(RadixTree):

    def _replace_child(self, parent, new_node):
        if parent is None:
            self.root = new_node
        else:
            key = new_node.prefix[0] if new_node.prefix else None
            parent.children[key] = new_node
            
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
                    n.count += 1
                    finished_adding_current_key = True
                else:  
                    i = self._get_common_prefix_length(n.prefix, key)
                    # Right now i can be the first difference, 
                    # len(key) or len(n.prefix)
                    if i == len(key):
                        # len(key) < len(n.prefix) AND key = n.prefix[:i]
                        m = SingleChildNode(n.prefix[:i], n.count + 1, True, n)
                        n.prefix = n.prefix[i:]
                        self._replace_child(n_parent, m)
                        finished_adding_current_key = True
                    elif i == len(n.prefix):
                        # len(key) > len(n.prefix) AND key[:i] = n.prefix
                        n.count += 1
                        if n.node_type == 0:
                            m = LeafNode(key[i:], 1)
                            new_n = SingleChildNode(n.prefix, n.count, True, m)
                            self._replace_child(n_parent, new_n)

                            finished_adding_current_key = True
                        elif n.node_type == 1:
                            if n.child.prefix[0] == key[i]:
                                n_parent = n
                                n = n.child
                                key = key[i:]
                                continue
                            else:
                                m = MultiChildNode(n.prefix, n.count, n.is_terminal)
                                m.children[n.child.prefix[0]] = n.child
                                m.children[key[i]] = LeafNode(key[i:], 1)
                                self._replace_child(n_parent, m)
                                finished_adding_current_key = True
                        elif n.node_type == 2:
                            if key[i] in n.children:
                                n_parent = n
                                n = n.children[key[i]]
                                key = key[i:]
                                continue
                            else:
                                m = LeafNode(key[i:], 1)
                                n.children[key[i]] = m
                                finished_adding_current_key = True
                    else:
                        # The first difference was found before 
                        # the end of key or n.prefix
                        m = MultiChildNode(n.prefix[:i], n.count + 1, False)
                        m.children[n.prefix[i]] = n
                        m.children[key[i]] = LeafNode(key[i:], 1)
                        self._replace_child(n_parent, m)
                        n.prefix = n.prefix[i:]
                        finished_adding_current_key = True

    def _compare_to(self, key1, key2, order):
        if key1 == key2: return 0
        if key1 is None: return -1
        # Assuming key2 will never be "None" based on the mining loop
        return -1 if order[key1] < order[key2] else 1

    def get_support_of_itemset(self, itemset: list, order):
        if not itemset: # Empty itemset case
            return self.root.count if self.root else 0
        # We start at the root having checked 0 items of the itemset
        return self._get_support_of_itemset_at_node(itemset, self.root, len(itemset) - 1, order)
    
    def _get_support_of_itemset_at_node(self, itemset, node, j, order):
        # Check the current node's prefix
        for i in range(0, len(node.prefix)):
            # Stop if we have already checked every item from the itemset
            if j < 0: 
                return node.count
            elif node.prefix[i] == itemset[j]:
                j -= 1 # We have to check the next item in the itemset
            elif self._compare_to(node.prefix[i], itemset[j], order) == 1: 
                # Entering here means that this node is missing some items of the itemset
                return 0
        # Stop if we have already checked every item from the itemset
        if j < 0: 
            return node.count
        
        # Now, if we didn't return, we must continue checking this node's children
        result = 0
        if node.node_type == 0:
            # Then it has no children, so we return while having not
            # found the full itemset
            return 0
        elif node.node_type == 1:
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
                  str(n.prefix) + ", support: " + str(n.count) + ")")
        elif isinstance(n, SingleChildNode):
            print(indentation + item + "├── (" + "--> " +
                  str(n.prefix) + ", support: " + str(n.count) + ")")
            label = n.child.prefix[0] if n.child.prefix else "[]"
            self._print(n.child, i+1, label)
        else:
            print(indentation + item + "├── (" + "--> " +
                  str(n.prefix) + ", support: " + str(n.count) + ")")
            for item, child in n.children.items():
                self._print(child, i+1, item)
        
    def print(self):
        self._print(self.root, 0, str(self.root.prefix))

    def count_nodes_and_max_depth(self):
        return self._count_nodes_and_max_depth(self.root)
    
    def _count_nodes_and_max_depth(self, node):
        # LeafNode
        if node.node_type == 0:
            return 1, 1
        
        # SingleChildNode
        if node.node_type == 1:
            child_count, child_depth = self._count_nodes_and_max_depth(node.child)
            return 1 + child_count, 1 + child_depth
        
        # MultiChildNode
        total_nodes = 1
        max_sub_depth = 1
        for child in node.children.values():
            c_count, c_depth = self._count_nodes_and_max_depth(child)
            total_nodes += c_count
            max_sub_depth = max(max_sub_depth, c_depth)
        
        return total_nodes, max_sub_depth

# example = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}]
#
#·├── (--> [], support: 3)
#       Atenas├── (--> ['Atenas'], support: 2)   
#              Roma├── (--> ['Roma'], support: 1)
# Using the order makes sure that if we see item1 and item4 and item5 as its children,
# item2 and item3 cannot be anywhere in the subtree