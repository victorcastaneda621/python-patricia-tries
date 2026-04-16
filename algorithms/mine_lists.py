from collections import Counter
import time

def select(D, X):
        out = []
        X = set(X)
        for tran in D:
            if X.issubset(tran):
                out.append(tran)
        return out

def mine_lists(transactions, min_supp):

    Dprime = transactions

    count = Counter()
    for t in transactions:
        for item in t:
            count[item] += 1
    IL = [item for item, _ in count.most_common()]
    X,h,l = [None for _ in IL],0,0

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

    return returned

