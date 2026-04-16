from algorithms.mine_radix import mine_radix
from data_structures import radix_tree_SN_TD, radix_tree_SN_BU, radix_tree_MN_TD, radix_tree_MN_BU
from data_structures.radix_tree.radix_tree_utils import radix_tree_count_sort

ALGORITHMS = {
    "radix-SN-BU": lambda t, m: mine_radix(t, m, single_node=True, top_down=False),
    "radix-SN-TD": lambda t, m: mine_radix(t, m, single_node=True, top_down=True),
    "radix-MN-BU": lambda t, m: mine_radix(t, m, single_node=False, top_down=False),
    "radix-MN-TD": lambda t, m: mine_radix(t, m, single_node=False, top_down=True)
}

transactions = [{"Atenas", "Oslo", "Roma", "Viena"}, {"Oslo"}, 
                            {"Oslo", "Roma", "Viena"}, {"Oslo"}, {"Londres", "Madrid"}, 
                            {"Londres", "Madrid", "Oslo"}]
transactions, count, order = radix_tree_count_sort(transactions)
print(order)

sntd = radix_tree_SN_TD.RadixTree_SN_TD()
snbu = radix_tree_SN_BU.RadixTree_SN_BU()
mntd = radix_tree_MN_TD.RadixTree_MN_TD()
mnbu = radix_tree_MN_BU.RadixTree_MN_BU()

for tree in [sntd, snbu, mntd, mnbu]:
    print(type(tree))
    tree.insert(transactions)
    print(tree.get_support_of_itemset(["Roma", "Londres"], order))
sntd.print()