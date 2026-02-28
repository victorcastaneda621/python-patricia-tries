from ucimlrepo import fetch_ucirepo 
import patricia_interface, patricia
  
# fetch dataset 
#mushroom = fetch_ucirepo(id=73)
#X = mushroom.data.features

def row_to_transaction(row):
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

#transactions = [row_to_transaction(row) for _, row in X.iterrows()]
transactions = [{"Atenas", "Oslo", "Roma", "Vienna"}, {"Atenas", "Oslo", "Roma", "Praga"}, {"Oslo", "Roma", "Vienna"}, {"Oslo"}]
support_dict = patricia_interface.count_support(transactions)
global_order, reverse_order = patricia_interface.generate_global_order_descending_support(support_dict)
sequence_list = patricia_interface.transactionListToSequences(transactions, global_order)

trie = patricia.trie()
for seq in sequence_list:
    trie[seq] = True

## PatriciaMine

Dprime = trie
IL = [item for item, _ in sorted(global_order.items(), key=lambda x: x[1])]
count = support_dict
X,h,l = [""] * len(IL),0,0
min_supp = 2

def select(D, X):
    out = patricia.trie()
    print(D)
    print(X)
    print(patricia_interface.transactionToBitSequence(X, global_order))
    print(list(D.iter(prefix=patricia_interface.transactionToBitSequence(X, global_order))))
    for t in list(D.iter(prefix=patricia_interface.transactionToBitSequence(X, global_order))):
        out[t] = True
    print(list(out.keys()))
    return out


while l<len(IL):
    print("X = %s, h = %s, l= %s"%("".join(X),h,l))
    input()
    if count[IL[l]] < min_supp:
        l += 1
    else:
        if h>0 and IL[l]==X[h-1]:
            print("if True",X)
            
            l += 1
            h -= 1
        else:
            X[h] = IL[l]
            h += 1
            print("if False, Generate","".join(X[:h]),X)

            if l:
                DX = select(Dprime,X[:h])
                print("    D'%s = %s\n"%("".join(X[:h]),DX))
            for i in range(l-1,-1,-1):
                
                print("    make %s.ptr point to head of threaded list for item %s w.r.t. D'%s"%(IL[i],IL[i],"".join(X[:h])))
                print("    %s.count =  support of %s item in D'%s"%(IL[i],IL[i],"".join(X[:h])))
                # Commenting the next line generates all the tree, not just frequent itemsets
                pos = global_order[IL[i]]
                count[IL[i]] = sum([1 for elem in DX if elem[pos] == "1"])
                print("    new support for ",IL[i],"is",count[IL[i]],"\n")
            l=0