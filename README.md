# python-patricia-tries

A Python implementation of two trie-based data structures (a trie is a prefix tree where each node contains one element from the prefix):

- **Radix trie**: Compressed trie, where strings of nodes with only one child are merged into a single node, storing a subsequence of the prefix in said node. Four variants were implemented (SN_TD, SN_BU, MN_TD, MN_BU):
  - `SN` (Single Node): all nodes share a single type. `MN` (Multi Node): leaf and internal nodes are distinct.
  - `TD` (Top-Down): support is calculated via top-down traversal. `BU` (Bottom-Up): support is calculated via bottom-up traversal.
- **Patricia trie**: Compressed binary trie, where prefixes are turned into their characteristic functions, and those are stored. Thus, bitwise operations can be used in place of set/list operations.

Two mining algorithms are implemented to test these structures:

- **PatriciaMine**: Frequent itemset mining (finds all itemsets meeting a minimum support threshold).
- **TopKMiner**: Frequent closed itemset mining (finds the top-K most frequent closed itemsets).

## References

- Pietracaprina, A., & Zandolin, D. (2003). *Mining Frequent Itemsets using Patricia Tries*. FIMI '03, Frequent Itemset Mining Implementations, ICDM 2003 Workshop, Melbourne, Florida. CEUR-WS.org. https://ceur-ws.org/Vol-90/pietracaprina.pdf
- Pietracaprina, A., & Vandin, F. (2007). *Efficient Incremental Mining of Top-K Frequent Closed Itemsets*. Discovery Science, Springer Berlin Heidelberg, pp. 275–280.

## Project Structure

```
├── PatriciaMine.py          # PatriciaMine caller (handles parameters, metrics, etc.)
├── TopKMiner.py             # Top-K caller (handles parameters, metrics, etc.)
├── general_utils.py         # Shared helpers (writing results/metrics to a file)
├── algorithms/
│   ├── mine_patricia.py     # PatriciaMine using a Patricia trie
│   ├── mine_radix.py        # PatriciaMine using the radix tree variants
│   ├── mine_lists.py        # PatriciaMine using a list (baseline for the testing)
│   ├── topk_patricia.py     # TopKMiner using a Patricia trie
│   ├── topk_radix.py        # TopKMiner using the radix tree variants
│   └── topk_lists.py        # TopKMiner using a list (baseline for the testing)
├── data_structures/         # Patricia trie and radix tree implementations
└── datasets/                # Raw .dat transaction files (mushroom, connect4, pumsb, etc.)
```

## Dependencies

No external libraries required (only Python standard libraries (`argparse`, `os`, `csv`) are used).

## Usage

**PatriciaMine**
```bash
python PatriciaMine.py --alg <algorithm> --data <dataset> --minsup <int> [--benchmark]
```
- `--alg` — which structure to use for mining
- `--data` — which dataset to load
- `--minsup` — minimum support threshold for an itemset to be considered frequent
- `--benchmark` — (optional) skips writing itemsets to a file, saving time

**TopKMiner**
```bash
python TopKMiner.py --alg <algorithm> --data <dataset> --k <int> [--benchmark]
```
- `--alg` — which structure to use for mining
- `--data` — which dataset to load
- `--k` — number of frequent closed itemsets to mine
- `--benchmark` — (optional) skips writing itemsets to a file, saving time

**Available options for both (extendable by adding new options to the callers):**

| | Options |
|---|---|
| `--alg` | `patricia`, `list`, `radix-SN-BU`, `radix-SN-TD`, `radix-MN-BU`, `radix-MN-TD` |
| `--data` | `mushroom`, `connect4`, `pumsb`, `pumsb_star`, `artificial_1`, `small_cities` |

## Output

Results are written to the `files/` directory (created automatically):
- `files/metrics_patricia_mine.csv` or `files/metrics_topk.csv`: timing and memory metrics for each run (data only collected in the `mem-benchmark` branch of the repository).
- `files/results/` — one `.txt` file per run containing the mined itemsets (e.g. `PM_patricia_mushroom_8000.txt`). Skipped when `--benchmark` is set.
- 
## Examples

Mine frequent itemsets from the mushroom dataset using a Patricia trie (mined itemsets ouputted to `PM_patricia_mushroom_8000.txt`):
```bash
python PatriciaMine.py --alg patricia --data mushroom --minsup 8000
```

Mine frequent itemsets from the mushroom dataset using the list baseline (mined itemsets ouputted to `PM_list_mushroom_8000.txt`):
```bash
python PatriciaMine.py --alg list --data mushroom --minsup 8000
```

Mine frequent itemsets from the connect4 dataset using a radix trie (SN_BU variant) in benchmark mode (no output file written):
```bash
python PatriciaMine.py --alg radix-SN-BU --data connect4 --minsup 1000 --benchmark
```

Mine the top 50 frequent closed itemsets from pumsb using the MN_BU radix variant (mined itemsets ouputted to `PM_radix-MN-BU_mushroom_8000.txt`):
```bash
python TopKMiner.py --alg radix-MN-BU --data pumsb --k 50
```

Mine the top 50 frequent closed itemsets from pumsb using a Patricia trie in benchmark mode (no output file written):
```bash
python TopKMiner.py --alg patricia --data pumsb --k 100 --benchmark
```