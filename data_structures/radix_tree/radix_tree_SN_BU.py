from data_structures.radix_tree.radix_tree_utils import NodeP, RadixTree
from collections import defaultdict

class SN_RadixNode(NodeP):
    __slots__ = ['children']
    def __init__(self, prefix: list, count: int, is_terminal: bool, parent: NodeP = None, children: dict = None):
        super().__init__(prefix, count, is_terminal, parent)
        self.children = children if children else {}

class RadixTree_SN_BU(RadixTree): 

    def _replace_child(self, parent, new_node):
        if parent is None:
            self.root = new_node
        else:
            key = new_node.prefix[0] if new_node.prefix else None
            parent.children[key] = new_node

    def build_node_lists(self):
        self.node_lists = defaultdict(list)
        self._build_node_lists(self.root)

    def _build_node_lists(self, node):
        if not node: 
            return
        for item in node.prefix:
            self.node_lists[item].append(node)
            
        for child in node.children.values():
            self._build_node_lists(child)

    def insert(self, keys: list):
        # Turn sets into lists (giving the items an order)
        # keys = [sorted(key) for key in keys]

        # If the tree is empty, we need to add the first item as root
        if not self.root:
            self.root = SN_RadixNode(keys[0], 1, True)
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
                        m = SN_RadixNode(n.prefix[:i], n.count + 1, True, n_parent, {n.prefix[i]:n})
                        n.parent = m
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
                            m = SN_RadixNode(key[i:], 1, True, n)
                            n.children[key[i]] = m
                            finished_adding_current_key = True
                    else:
                        # The first difference was found before 
                        # the end of key or n.prefix
                        m = SN_RadixNode(n.prefix[:i], n.count + 1, False, n_parent)
                        m.children[n.prefix[i]] = n
                        n.parent = m
                        m.children[key[i]] = SN_RadixNode(key[i:], 1, True, m)
                        self._replace_child(n_parent, m)
                        n.prefix = n.prefix[i:]
                        finished_adding_current_key = True
        self.build_node_lists()

    def _compare_to(self, key1, key2, order):
        if key1 == key2: return 0
        if key1 is None: return -1
        # Assuming key2 will never be "None" based on the mining loop
        return -1 if order[key1] < order[key2] else 1

    def get_support_of_itemset(self, itemset: list, _order):
        if not itemset:
            return self.root.count if self.root else 0
        
        target_item = itemset[0]
        if target_item not in self.node_lists:
            return 0
        
        itemset_set = set(itemset)
        target_len = len(itemset_set)
        total_support = 0
        
        for node in self.node_lists[target_item]:
            current = node
            found_count = 0
            
            while current is not None:
                for p_item in current.prefix:
                    if p_item in itemset_set:
                        found_count += 1
                
                if found_count == target_len:
                    break
                current = current.parent

            if found_count == target_len:
                total_support += node.count
                
        return total_support
        
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

    def get_closure(self, itemset, order):
        if not self.root:
            return set(), 0
        if not itemset:
            # closure of empty set: items in every transaction
            item_counts = {}
            supp = self.root.count
            self._count_items_downward(self.root, item_counts)
            closure = {item for item, count in item_counts.items() if count == supp}
            return closure, supp

        target_item = itemset[0]  # least frequent (reverse sorted)
        if target_item not in self.node_lists:
            return set(), 0

        itemset_set = set(itemset)
        target_len = len(itemset_set)
        extension_item = itemset[0]
        item_counts = {}
        total_support = 0

        for node in self.node_lists[target_item]:
            # walk up verifying all itemset items are on this path
            current = node
            found_count = 0
            path_items = set()

            while current is not None:
                for p_item in current.prefix:
                    path_items.add(p_item)
                    if p_item in itemset_set:
                        found_count += 1
                if found_count == target_len:
                    break
                current = current.parent

            if found_count != target_len:
                continue  # this branch doesn't contain the full itemset

            # ppc check: no item more frequent than extension_item
            # on the path that isn't in the itemset
            ppc_ok = True
            for p_item in path_items:
                if p_item not in itemset_set and order[p_item] < order[extension_item]:
                    ppc_ok = False
                    break

            if not ppc_ok:
                continue

            # walk down from node collecting co-occurring items
            node_item_counts = {}
            self._count_items_downward(node, node_item_counts)
            # also add path items above node (ancestors already verified)
            ancestor = node.parent
            while ancestor is not None:
                for p_item in ancestor.prefix:
                    node_item_counts[p_item] = node_item_counts.get(p_item, 0) + node.count
                ancestor = ancestor.parent

            for item, count in node_item_counts.items():
                item_counts[item] = item_counts.get(item, 0) + count
            total_support += node.count

        if total_support == 0:
            return set(), 0

        closure = set(itemset)
        for item, count in item_counts.items():
            if count == total_support:
                closure.add(item)
        return closure, total_support

    def _count_items_downward(self, node, item_counts):
        for item in node.prefix:
            item_counts[item] = item_counts.get(item, 0) + node.count
        for child in node.children.values():
            self._count_items_downward(child, item_counts)

    def get_support_and_ppc_check(self, itemset, order):
        if not itemset:
            return self.root.count if self.root else 0, True
        target_item = itemset[0]
        if target_item not in self.node_lists:
            return 0, True
        itemset_set = set(itemset)
        target_len = len(itemset_set)
        extension_item = itemset[0]
        total_support = 0

        for node in self.node_lists[target_item]:
            current = node
            found_count = 0
            path_items = set()
            while current is not None:
                for p_item in current.prefix:
                    path_items.add(p_item)
                    if p_item in itemset_set:
                        found_count += 1
                if found_count == target_len:
                    break
                current = current.parent
            if found_count != target_len:
                continue
            # ppc check
            for p_item in path_items:
                if p_item not in itemset_set and order[p_item] < order[extension_item]:
                    return 0, False
            total_support += node.count

        return total_support, True

    def get_support_ppc_and_closure(self, itemset, order):
        if not itemset:
            return self.root.count if self.root else 0, True, set()
        target_item = itemset[0]
        if target_item not in self.node_lists:
            return 0, True, set()
        itemset_set = set(itemset)
        target_len = len(itemset_set)
        extension_item = itemset[0]
        item_counts = {}
        total_support = 0

        for node in self.node_lists[target_item]:
            current = node
            found_count = 0
            path_items = set()
            while current is not None:
                for p_item in current.prefix:
                    path_items.add(p_item)
                    if p_item in itemset_set:
                        found_count += 1
                if found_count == target_len:
                    break
                current = current.parent
            if found_count != target_len:
                continue
            # ppc check
            ppc_ok = True
            for p_item in path_items:
                if p_item not in itemset_set and order[p_item] < order[extension_item]:
                    return 0, False, set()
            # collect items downward
            node_item_counts = {}
            self._count_items_downward(node, node_item_counts)
            ancestor = node.parent
            while ancestor is not None:
                for p_item in ancestor.prefix:
                    node_item_counts[p_item] = node_item_counts.get(p_item, 0) + node.count
                ancestor = ancestor.parent
            for item, count in node_item_counts.items():
                item_counts[item] = item_counts.get(item, 0) + count
            total_support += node.count

        if total_support == 0:
            return 0, True, set()
        closure = set(itemset)
        for item, count in item_counts.items():
            if count == total_support:
                closure.add(item)
        return total_support, True, closure