#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 70:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-39

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    # ---------------- MUSHROOM (minsup = 640) ----------------
    0) ALG="radix-SN-TD"; DATASET="mushroom"; MINSUP=640; BENCH="--benchmark" ;; # Sin returned
    1) ALG="radix-SN-TD"; DATASET="mushroom"; MINSUP=640; BENCH=""            ;; # Con returned
    2) ALG="radix-SN-BU"; DATASET="mushroom"; MINSUP=640; BENCH="--benchmark" ;; # Sin returned
    3) ALG="radix-SN-BU"; DATASET="mushroom"; MINSUP=640; BENCH=""            ;; # Con returned
    4) ALG="radix-MN-TD"; DATASET="mushroom"; MINSUP=640; BENCH="--benchmark" ;; # Sin returned
    5) ALG="radix-MN-TD"; DATASET="mushroom"; MINSUP=640; BENCH=""            ;; # Con returned
    6) ALG="radix-MN-BU"; DATASET="mushroom"; MINSUP=640; BENCH="--benchmark" ;; # Sin returned
    7) ALG="radix-MN-BU"; DATASET="mushroom"; MINSUP=640; BENCH=""            ;; # Con returned

    # ---------------- CONNECT-4 (minsup = 44535) ----------------
    8)  ALG="radix-SN-TD"; DATASET="connect4"; MINSUP=44535; BENCH="--benchmark" ;; # Sin returned
    9)  ALG="radix-SN-TD"; DATASET="connect4"; MINSUP=44535; BENCH=""            ;; # Con returned
    10) ALG="radix-SN-BU"; DATASET="connect4"; MINSUP=44535; BENCH="--benchmark" ;; # Sin returned
    11) ALG="radix-SN-BU"; DATASET="connect4"; MINSUP=44535; BENCH=""            ;; # Con returned
    12) ALG="radix-MN-TD"; DATASET="connect4"; MINSUP=44535; BENCH="--benchmark" ;; # Sin returned
    13) ALG="radix-MN-TD"; DATASET="connect4"; MINSUP=44535; BENCH=""            ;; # Con returned
    14) ALG="radix-MN-BU"; DATASET="connect4"; MINSUP=44535; BENCH="--benchmark" ;; # Sin returned
    15) ALG="radix-MN-BU"; DATASET="connect4"; MINSUP=44535; BENCH=""            ;; # Con returned

    # ---------------- PUMSB (minsup = 35000) ----------------
    16) ALG="radix-SN-TD"; DATASET="pumsb"; MINSUP=35000; BENCH="--benchmark" ;; # Sin returned
    17) ALG="radix-SN-TD"; DATASET="pumsb"; MINSUP=35000; BENCH=""            ;; # Con returned
    18) ALG="radix-SN-BU"; DATASET="pumsb"; MINSUP=35000; BENCH="--benchmark" ;; # Sin returned
    19) ALG="radix-SN-BU"; DATASET="pumsb"; MINSUP=35000; BENCH=""            ;; # Con returned
    20) ALG="radix-MN-TD"; DATASET="pumsb"; MINSUP=35000; BENCH="--benchmark" ;; # Sin returned
    21) ALG="radix-MN-TD"; DATASET="pumsb"; MINSUP=35000; BENCH=""            ;; # Con returned
    22) ALG="radix-MN-BU"; DATASET="pumsb"; MINSUP=35000; BENCH="--benchmark" ;; # Sin returned
    23) ALG="radix-MN-BU"; DATASET="pumsb"; MINSUP=35000; BENCH=""            ;; # Con returned

    # ---------------- PUMSB* (minsup = 14000) ----------------
    24) ALG="radix-SN-TD"; DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;; # Sin returned
    25) ALG="radix-SN-TD"; DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;; # Con returned
    26) ALG="radix-SN-BU"; DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;; # Sin returned
    27) ALG="radix-SN-BU"; DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;; # Con returned
    28) ALG="radix-MN-TD"; DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;; # Sin returned
    29) ALG="radix-MN-TD"; DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;; # Con returned
    30) ALG="radix-MN-BU"; DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;; # Sin returned
    31) ALG="radix-MN-BU"; DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;; # Con returned

    # ---------------- T10.I4.D100k (minsup = 200) ----------------
    32) ALG="radix-SN-TD"; DATASET="artificial_1"; MINSUP=200; BENCH="--benchmark" ;; # Sin returned
    33) ALG="radix-SN-TD"; DATASET="artificial_1"; MINSUP=200; BENCH=""            ;; # Con returned
    34) ALG="radix-SN-BU"; DATASET="artificial_1"; MINSUP=200; BENCH="--benchmark" ;; # Sin returned
    35) ALG="radix-SN-BU"; DATASET="artificial_1"; MINSUP=200; BENCH=""            ;; # Con returned
    36) ALG="radix-MN-TD"; DATASET="artificial_1"; MINSUP=200; BENCH="--benchmark" ;; # Sin returned
    37) ALG="radix-MN-TD"; DATASET="artificial_1"; MINSUP=200; BENCH=""            ;; # Con returned
    38) ALG="radix-MN-BU"; DATASET="artificial_1"; MINSUP=200; BENCH="--benchmark" ;; # Sin returned
    39) ALG="radix-MN-BU"; DATASET="artificial_1"; MINSUP=200; BENCH=""
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP $BENCH"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" $BENCH

echo "Finished"