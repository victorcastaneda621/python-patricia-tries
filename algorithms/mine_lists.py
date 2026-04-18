from collections import Counter
import time
from general_utils import prune_dataset
#import tracemalloc

def select(D, X):
        out = []
        X = set(X)
        for tran in D:
            if X.issubset(tran):
                out.append(tran)
        return out

def mine_lists(transactions, min_supp):
    before_build = time.perf_counter()
    #tracemalloc.start()

    transactions = prune_dataset(transactions, min_supp)

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
                returned.append(X[:h])

                if l:
                    DX = select(transactions,X[:h])
                for i in range(l-1,-1,-1):
                    count[IL[i]] = sum([1 for elem in DX if IL[i] in elem])
                l=0

    after_mining = time.perf_counter()
    #current, peak = tracemalloc.get_traced_memory()
    #peak_memory_mb = peak / (1024 * 1024)
    #tracemalloc.stop()
    #print("peak_memory_mb: " + str(peak_memory_mb))
    return {"build_time": after_build - before_build,
            "mining_time": after_mining - after_build,
            "itemsets": returned,
            "node_count": "-",
            "max_depth": "-",
            "peak_memory_mb": "-",
            "tree_size_mb":"-"
            }

