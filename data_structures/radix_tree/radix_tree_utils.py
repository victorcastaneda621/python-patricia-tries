from collections import Counter

def radix_tree_count_sort(transaction_list: list):
    support = Counter()
    for t in transaction_list:
        support.update(t)

    order = {item:i for i, (item, _) in enumerate(support.most_common())}

    for i in range(len(transaction_list)):
        transaction_list[i] = sorted(transaction_list[i], key=order.get)

    return transaction_list, support, order

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

class Node():
    __slots__ = ['prefix', 'count', 'is_terminal']
    def __init__(self, prefix: list, count: int, is_terminal: bool):
        self.prefix = prefix
        self.count = count
        self.is_terminal = is_terminal

class NodeP(Node):
    __slots__ = ['parent']
    def __init__(self, prefix: list, count: int, is_terminal: bool, parent: Node):
        super().__init__(prefix, count, is_terminal)
        self.parent = parent

class LeafNodeP(NodeP):
    __slots__ = ['node_type']
    def __init__(self, prefix: list, count: int):
        super().__init__(prefix, count, True)
        self.node_type = 0

class SingleChildNodeP(NodeP):
    __slots__ = ['child', 'node_type']
    def __init__(self, prefix: list, count: int, is_terminal: bool, child: Node = None):
        super().__init__(prefix, count, is_terminal)
        self.child = child
        self.node_type = 1

class MultiChildNodeP(SN_RadixNodeP):
    __slots__ = ['node_type']
    def __init__(self, prefix: list, count: int, is_terminal: bool, children: dict = None):
        super().__init__(prefix, count, is_terminal, children)
        self.node_type = 2