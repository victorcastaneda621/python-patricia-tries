from ucimlrepo import fetch_ucirepo
from collections import Counter
import time

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

Dprime = transactions

after_trie_build = time.perf_counter()

count = Counter()
for t in transactions:
    for item in t:
        count[item] += 1
IL = [item for item, _ in count.most_common()]
X,h,l = [None for _ in IL],0,0
min_supp = 1000

def select(D, X):
    out = []
    X = set(X)
    for tran in D:
        if X.issubset(tran):
            out.append(tran)
    return out

returned = []
while l<len(IL):
    if count[IL[l]] < min_supp:
        l += 1
    else:
        if h>0 and IL[l]==X[h-1]:
            
            l += 1
            h -= 1
        else:
            X[h] = IL[l]
            h += 1
            #print("Generate","".join(X[:h]),X)
            returned.append(X[:h])

            if l:
                DX = select(Dprime,X[:h])
            for i in range(l-1,-1,-1):
                count[IL[i]] = sum([1 for elem in DX if IL[i] in elem])
            l=0

after_mining = time.perf_counter()
print("----------------------------------------------------------------\n")
print("Returned: ", returned)
print("Times:\n - Trie Building: " + str(after_trie_build - before_trie_build) + "\n - Mining: " + str(after_mining - after_trie_build))

