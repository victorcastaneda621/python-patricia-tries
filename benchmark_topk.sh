#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 100:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-59

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    0) ALG="radix-SN-TD"; DATASET="mushroom"; K=50000; BENCH="" ;;
    1) ALG="radix-SN-BU"; DATASET="mushroom"; K=50000; BENCH="" ;;
    2) ALG="radix-MN-TD"; DATASET="mushroom"; K=50000; BENCH="" ;;
    3) ALG="radix-MN-BU"; DATASET="mushroom"; K=50000; BENCH="" ;;
    4) ALG="patricia";    DATASET="mushroom"; K=50000; BENCH="" ;;
    5) ALG="list";        DATASET="mushroom"; K=50000; BENCH="" ;;

    6) ALG="radix-SN-TD"; DATASET="connect4"; K=50000; BENCH="" ;;
    7) ALG="radix-SN-BU"; DATASET="connect4"; K=50000; BENCH="" ;;
    8) ALG="radix-MN-TD"; DATASET="connect4"; K=50000; BENCH="" ;;
    9) ALG="radix-MN-BU"; DATASET="connect4"; K=50000; BENCH="" ;;
    10) ALG="patricia";   DATASET="connect4"; K=50000; BENCH="" ;;
    11) ALG="list";       DATASET="connect4"; K=50000; BENCH="" ;;

    12) ALG="radix-SN-TD"; DATASET="pumsb"; K=35000; BENCH="" ;;
    13) ALG="radix-SN-BU"; DATASET="pumsb"; K=35000; BENCH="" ;;
    14) ALG="radix-MN-TD"; DATASET="pumsb"; K=35000; BENCH="" ;;
    15) ALG="radix-MN-BU"; DATASET="pumsb"; K=35000; BENCH="" ;;
    16) ALG="patricia";    DATASET="pumsb"; K=35000; BENCH="" ;;
    17) ALG="list";        DATASET="pumsb"; K=35000; BENCH="" ;;

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

    30) ALG="radix-SN-TD"; DATASET="mushroom"; K=50000; BENCH="--benchmark" ;;
    31) ALG="radix-SN-BU"; DATASET="mushroom"; K=50000; BENCH="--benchmark" ;;
    32) ALG="radix-MN-TD"; DATASET="mushroom"; K=50000; BENCH="--benchmark" ;;
    33) ALG="radix-MN-BU"; DATASET="mushroom"; K=50000; BENCH="--benchmark" ;;
    34) ALG="patricia";    DATASET="mushroom"; K=50000; BENCH="--benchmark" ;;
    35) ALG="list";        DATASET="mushroom"; K=50000; BENCH="--benchmark" ;;

    36) ALG="radix-SN-TD"; DATASET="connect4"; K=50000; BENCH=--benchmark"" ;;
    37) ALG="radix-SN-BU"; DATASET="connect4"; K=50000; BENCH="--benchmark" ;;
    38) ALG="radix-MN-TD"; DATASET="connect4"; K=50000; BENCH="--benchmark" ;;
    39) ALG="radix-MN-BU"; DATASET="connect4"; K=50000; BENCH="--benchmark" ;;
    40) ALG="patricia";   DATASET="connect4"; K=50000; BENCH="--benchmark" ;;
    41) ALG="list";       DATASET="connect4"; K=50000; BENCH="--benchmark" ;;

    42) ALG="radix-SN-TD"; DATASET="pumsb"; K=35000; BENCH="--benchmark" ;;
    43) ALG="radix-SN-BU"; DATASET="pumsb"; K=35000; BENCH="--benchmark" ;;
    44) ALG="radix-MN-TD"; DATASET="pumsb"; K=35000; BENCH="--benchmark" ;;
    45) ALG="radix-MN-BU"; DATASET="pumsb"; K=35000; BENCH="--benchmark" ;;
    46) ALG="patricia";    DATASET="pumsb"; K=35000; BENCH="--benchmark" ;;
    47) ALG="list";        DATASET="pumsb"; K=35000; BENCH="--benchmark" ;;

    48) ALG="radix-SN-TD"; DATASET="pumsb_star"; K=35000; BENCH="--benchmark" ;;
    49) ALG="radix-SN-BU"; DATASET="pumsb_star"; K=35000; BENCH="--benchmark" ;;
    50) ALG="radix-MN-TD"; DATASET="pumsb_star"; K=35000; BENCH="--benchmark" ;;
    51) ALG="radix-MN-BU"; DATASET="pumsb_star"; K=35000; BENCH="--benchmark" ;;
    52) ALG="patricia";    DATASET="pumsb_star"; K=35000; BENCH="--benchmark" ;;
    53) ALG="list";        DATASET="pumsb_star"; K=35000; BENCH="--benchmark" ;;

    54) ALG="radix-SN-TD"; DATASET="artificial_1"; K=2500; BENCH="--benchmark" ;;
    55) ALG="radix-SN-BU"; DATASET="artificial_1"; K=2500; BENCH="--benchmark" ;;
    56) ALG="radix-MN-TD"; DATASET="artificial_1"; K=2500; BENCH="--benchmark" ;;
    57) ALG="radix-MN-BU"; DATASET="artificial_1"; K=2500; BENCH="--benchmark" ;;
    58) ALG="patricia";    DATASET="artificial_1"; K=2500; BENCH="--benchmark" ;;
    59) ALG="list";        DATASET="artificial_1"; K=2500; BENCH="--benchmark" ;;
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | K=$K | " $BENCH

timeout 600000 python3 TopKMiner.py --alg "$ALG" --data "$DATASET" --k "$K" $BENCH

echo "Finished"