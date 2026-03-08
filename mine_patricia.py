from collections import Counter
from ucimlrepo import fetch_ucirepo
import time

import patricia_trie as pt

def row_to_transaction(row):
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

### Small example dataset #################################################################
#transactions = [{"Atenas", "Oslo", "Roma", "Viena"}, {"Oslo"}, 
#                {"Oslo", "Roma", "Viena"}, {"Oslo"}, {"Londres", "Madrid"}, 
#                {"Londres", "Madrid", "Oslo"}]
### Fetch mushroom dataset ################################################################# 
mushroom = fetch_ucirepo(id=73)
X = mushroom.data.features
### Fetch connect-4 dataset ################################################################# 
#connect_4 = fetch_ucirepo(id=26)
#X = connect_4.data.features

before_trie_build = time.perf_counter()
transactions = [row_to_transaction(row) for _, row in X.iterrows()]

trie = pt.PatriciaTrie()
trie.insert(transactions)
#print(trie.count_nodes())
#trie.print()

after_trie_build = time.perf_counter()

universe = [item for t in transactions for item in t] # The trie already does this and Count(universe), we should reuse it
#print(trie.get_support_of_itemset({"Atenas", "Londres", "Roma", "Viena"}))
IL = trie.index_to_item
count = Counter(universe)
X,h,l = ["" for i in IL],0,0
min_supp = 100

returned = []
while l<len(IL):
    #print("X = %s, h = %s, l= %s"%("".join(X),h,l))
    #input()
    if count[IL[l]] < min_supp:
        l += 1
    else:
        if h>0 and IL[l]==X[h-1]:
            #print("if True",X)
            
            l += 1
            h -= 1
        else:
            X[h] = IL[l]
            h += 1
            print("Generate","".join(X[:h]),X)
            returned.append(X[:h])

            for i in range(l-1,-1,-1):
                
                #print("    make %s.ptr point to head of threaded list for item %s w.r.t. D'%s"%(IL[i],IL[i],"".join(X[:h])))
                #print("    %s.count =  support of %s item in D'%s"%(IL[i],IL[i],"".join(X[:h])))
                # Commenting the next line generates all the tree, not just frequent itemsets
                count[IL[i]] = trie.get_support_of_itemset(set([IL[i]]) | set(X[:h]))
                #print("    new support for ",IL[i],"is",count[IL[i]],"\n")
            l=0
after_mining = time.perf_counter()
print("----------------------------------------------------------------\n")
print("Returned: ", returned)
print("Times:\n - Trie Building: " + str(after_trie_build - before_trie_build) + "\n - Mining: " + str(after_mining - after_trie_build))
