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
    0) ALG="patricia"; DATASET="mushroom"; MINSUP=640; BENCH="--benchmark" ;;
    1) ALG="patricia"; DATASET="mushroom"; MINSUP=640; BENCH=""            ;;
    2) ALG="list";     DATASET="mushroom"; MINSUP=640; BENCH="--benchmark" ;;
    3) ALG="list";     DATASET="mushroom"; MINSUP=640; BENCH=""            ;;

    # ---------------- CONNECT-4 (minsup = 44535) ----------------
    4) ALG="patricia"; DATASET="connect4"; MINSUP=44535; BENCH="--benchmark" ;;
    5) ALG="patricia"; DATASET="connect4"; MINSUP=44535; BENCH=""            ;;
    6) ALG="list";     DATASET="connect4"; MINSUP=44535; BENCH="--benchmark" ;;
    7) ALG="list";     DATASET="connect4"; MINSUP=44535; BENCH=""            ;;

    # ---------------- PUMSB (minsup = 35000) ----------------
    8)  ALG="patricia"; DATASET="pumsb"; MINSUP=35000; BENCH="--benchmark" ;;
    9)  ALG="patricia"; DATASET="pumsb"; MINSUP=35000; BENCH=""            ;;
    10) ALG="list";     DATASET="pumsb"; MINSUP=35000; BENCH="--benchmark" ;;
    11) ALG="list";     DATASET="pumsb"; MINSUP=35000; BENCH=""            ;;

    # ---------------- PUMSB* (minsup = 14000) ----------------
    12) ALG="patricia"; DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;;
    13) ALG="patricia"; DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;;
    14) ALG="list";     DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;;
    15) ALG="list";     DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;;

    # ---------------- T10.I4.D100k (minsup = 200) ----------------
    16) ALG="patricia"; DATASET="artificial_1"; MINSUP=200; BENCH="--benchmark" ;;
    17) ALG="patricia"; DATASET="artificial_1"; MINSUP=200; BENCH=""            ;;
    18) ALG="list";     DATASET="artificial_1"; MINSUP=200; BENCH="--benchmark" ;;
    19) ALG="list";     DATASET="artificial_1"; MINSUP=200; BENCH=""            ;;
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP $BENCH"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" $BENCH

echo "Finished"