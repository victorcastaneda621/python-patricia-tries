
class RadixNode():
    __slots__ = ['children', 'prefix', 'count', 'is_terminal']
    def __init__(self, prefix: list, count: int, is_terminal: bool, children: dict = None):
        self.children = children if children else {}
        self.prefix = prefix
        self.count = count
        self.is_terminal = is_terminal

## RADIX TREE ##############################################################

class RadixTreeSingleNode():
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
        else:
            key = new_node.prefix[0] if new_node.prefix else None
            parent.children[key] = new_node
            
    def insert(self, keys: list):
        # Turn sets into lists (giving the items an order)
        # keys = [sorted(key) for key in keys]

        # If the tree is empty, we need to add the first item as root
        if not self.root:
            self.root = RadixNode(keys[0], 1, True)
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
                        m = RadixNode(n.prefix[:i], n.count + 1, True, {n.prefix[i]:n})
                        n.prefix = n.prefix[i:]
                        self._replace_child(n_parent, m)
                        finished_adding_current_key = True
                    elif i == len(n.prefix):
                        # len(key) > len(n.prefix) AND key[:i] = n.prefix
                        n.count += 1
                        if key[i] in n.children:
                            n_parent = n
                            n = n.children[key[i]]
                            key = key[i:]
                            continue
                        else:
                            m = RadixNode(key[i:], 1, True)
                            n.children[key[i]] = m
                            finished_adding_current_key = True
                    else:
                        # The first difference was found before 
                        # the end of key or n.prefix
                        m = RadixNode(n.prefix[:i], n.count + 1, False)
                        m.children[n.prefix[i]] = n
                        m.children[key[i]] = RadixNode(key[i:], 1, True)
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
        # We start at the root with all items of the itemset needing to be checked
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
        if not node.children:
            # Then it has no children, so we return while having not
            # found the full itemset
            return 0
        else:
            # We check any of its children if it looks promising
            for child_key in node.children.keys():
                if self._compare_to(child_key, itemset[j], order) != 1:
                    result += self._get_support_of_itemset_at_node(
                        itemset, node.children[child_key], j, order)
        return result
    
    def get_support_t_list(item, itemset, tlist):
        #basically you get tlist[item] = {node1, node3}. You follow those pointers and traverse upwards
        # (we need node.parent). If you find everything else in itemsets, you add nodeX.count.
        pass
        
    def _print(self, n, i, item):
        indentation = "       " * i
        if not n.children:
            print(indentation + item + "├── (" + "--> " +
                  str(n.prefix) + ", count: " + str(n.count) + ")")
        else:
            print(indentation + item + "├── (" + "--> " +
                  str(n.prefix) + ", count: " + str(n.count) + ")")
            for item, child in n.children.items():
                self._print(child, i+1, item)
        
    def print(self):
        self._print(self.root, 0, str(self.root.prefix))

    def count_nodes_and_max_depth(self):
        return self._count_nodes_and_max_depth(self.root)
    
    def _count_nodes_and_max_depth(self, node):
        if not node.children:
            return (1, 1)
        else: 
            total_nodes = 1
            max_depth = 1
    
            for child in node.children.values():
                child_count, child_depth = self._count_nodes_and_max_depth(child)
                total_nodes += child_count
                max_depth = max(max_depth, child_depth)

            return total_nodes, max_depth
    
    def count_total_elements(self):
        if not self.root:
            return 0
        return self._count_total_elements(self.root)

    def _count_total_elements(self, node):
        # We count all elements on this node's prefix
        total = len(node.prefix)
        
        if not node.children: # Leaf
            return total
        else:
            for child in node.children.values():
                total += self._count_total_elements(child)
            return total

# example = [{"Atenas", "Oslo", "Roma"}, {"Atenas", "Oslo"}, {"Oslo"}]
#
#·├── (--> [], support: 3)
#       Atenas├── (--> ['Atenas'], support: 2)   
#              Roma├── (--> ['Roma'], support: 1)
# Using the order makes sure that if we see item1 and item4 and item5 as its children,
# item2 and item3 cannot be anywhere in the subtree