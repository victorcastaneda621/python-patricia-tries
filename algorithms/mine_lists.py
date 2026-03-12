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
    before_build = time.perf_counter()

    Dprime = transactions

    count = Counter()
    for t in transactions:
        for item in t:
            count[item] += 1
    IL = [item for item, _ in count.most_common()]
    X,h,l = [None for _ in IL],0,0

    after_build = time.perf_counter()

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
    return {"build_time": after_build - before_build,
            "mining_time": after_mining - after_build,
            "itemsets": returned}

