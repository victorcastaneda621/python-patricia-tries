#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 100:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-29

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    0) ALG="radix-SN-TD"; DATASET="mushroom"; K=50000; BENCH="" ;;
    1) ALG="radix-SN-BU"; DATASET="mushroom"; K=50000; BENCH="" ;;
    2) ALG="radix-MN-TD"; DATASET="mushroom"; K=50000; BENCH="" ;;
    3) ALG="radix-MN-BU"; DATASET="mushroom"; K=50000; BENCH="" ;;
    4) ALG="patricia";    DATASET="mushroom"; K=50000; BENCH="" ;;
    5) ALG="list";        DATASET="mushroom"; K=50000; BENCH="" ;;

    6) ALG="radix-SN-TD"; DATASET="connect4"; K=200000; BENCH="" ;;
    7) ALG="radix-SN-BU"; DATASET="connect4"; K=200000; BENCH="" ;;
    8) ALG="radix-MN-TD"; DATASET="connect4"; K=200000; BENCH="" ;;
    9) ALG="radix-MN-BU"; DATASET="connect4"; K=200000; BENCH="" ;;
    10) ALG="patricia";   DATASET="connect4"; K=200000; BENCH="" ;;
    11) ALG="list";       DATASET="connect4"; K=200000; BENCH="" ;;

    12) ALG="radix-SN-TD"; DATASET="pumsb"; K=100000; BENCH="" ;;
    13) ALG="radix-SN-BU"; DATASET="pumsb"; K=100000; BENCH="" ;;
    14) ALG="radix-MN-TD"; DATASET="pumsb"; K=100000; BENCH="" ;;
    15) ALG="radix-MN-BU"; DATASET="pumsb"; K=100000; BENCH="" ;;
    16) ALG="patricia";    DATASET="pumsb"; K=100000; BENCH="" ;;
    17) ALG="list";        DATASET="pumsb"; K=100000; BENCH="" ;;

    18) ALG="radix-SN-TD"; DATASET="pumsb_star"; K=35000; BENCH="" ;;
    19) ALG="radix-SN-BU"; DATASET="pumsb_star"; K=35000; BENCH="" ;;
    20) ALG="radix-MN-TD"; DATASET="pumsb_star"; K=35000; BENCH="" ;;
    21) ALG="radix-MN-BU"; DATASET="pumsb_star"; K=35000; BENCH="" ;;
    22) ALG="patricia";    DATASET="pumsb_star"; K=35000; BENCH="" ;;
    23) ALG="list";        DATASET="pumsb_star"; K=35000; BENCH="" ;;

    24) ALG="radix-SN-TD"; DATASET="artificial_1"; K=2500; BENCH="" ;;
    25) ALG="radix-SN-BU"; DATASET="artificial_1"; K=2500; BENCH="" ;;
    26) ALG="radix-MN-TD"; DATASET="artificial_1"; K=2500; BENCH="" ;;
    27) ALG="radix-MN-BU"; DATASET="artificial_1"; K=2500; BENCH="" ;;
    28) ALG="patricia";    DATASET="artificial_1"; K=2500; BENCH="" ;;
    29) ALG="list";        DATASET="artificial_1"; K=2500; BENCH="" ;;
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | K=$k | " $BENCH

python3 TopKMiner.py --alg "$ALG" --data "$DATASET" --k "$k" $BENCH

echo "Finished"