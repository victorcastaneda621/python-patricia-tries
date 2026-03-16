# python-patricia-tries

## Example Usage

```bash
python main.py --alg list --data mushroom --minsup 8000
```

```
Build time: 0.026363000040873885 s
Mining time: 1.4899997040629387e-05 s
Total time: 0.026377900037914515 s
Number of frequent itemsets: 1
```

```bash
python main.py --alg patricia --data mushroom --minsup 8000
```

```
Build time: 0.07911530020646751 s
Mining time: 2.1999934688210487e-05 s
Total time: 0.07913730014115572 s
Number of frequent itemsets: 1
```

```bash
python main.py --alg radix --data mushroom --minsup 8000
```

```
Build time: 0.046126100001856685 s
Mining time: 2.1799933165311813e-05 s
Total time: 0.046147899935021996 s
Number of frequent itemsets: 1
```

## General Usage

```bash
python main.py --alg {patricia,list,radix} \
               --data {mushroom_fimi,small_cities,connect4,connect4_fimi,pumsb,mushroom,artificial_1} \
               --minsup MINSUP
```