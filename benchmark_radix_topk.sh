#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 24:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-19

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    0)
        ALG="radix-MN-TD"
        DATASET="mushroom"
        k=915325
        ;;
    1)
        ALG="radix-MN-TD"
        DATASET="connect4"
        k=8368159
        ;;
    2)
        ALG="radix-MN-TD"
        DATASET="pumsb"
        k=1897479
        ;;
    3)
        ALG="radix-MN-TD"
        DATASET="pumsb_star"
        k=665683
        ;;
    4)
        ALG="radix-MN-TD"
        DATASET="artificial_1"
        k=13255
        ;;
    5)
        ALG="radix-MN-BU"
        DATASET="mushroom"
        k=915325
        ;;
    6)
        ALG="radix-MN-BU"
        DATASET="connect4"
        k=8368159
        ;;
    7)
        ALG="radix-MN-BU"
        DATASET="pumsb"
        k=1897479
        ;;
    8)
        ALG="radix-MN-BU"
        DATASET="pumsb_star"
        k=665683
        ;;
    9)
        ALG="radix-MN-BU"
        DATASET="artificial_1"
        k=13255
        ;;
    10)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        k=915325
        ;;
    11)
        ALG="radix-SN-TD"
        DATASET="connect4"
        k=8368159
        ;;
    12)
        ALG="radix-SN-TD"
        DATASET="pumsb"
        k=1897479
        ;;
    13)
        ALG="radix-SN-TD"
        DATASET="pumsb_star"
        k=665683
        ;;
    14)
        ALG="radix-SN-TD"
        DATASET="artificial_1"
        k=13255
        ;;
    15)
        ALG="radix-SN-BU"
        DATASET="mushroom"
        k=915325
        ;;
    16)
        ALG="radix-SN-BU"
        DATASET="connect4"
        k=8368159
        ;;
    17)
        ALG="radix-SN-BU"
        DATASET="pumsb"
        k=1897479
        ;;
    18)
        ALG="radix-SN-BU"
        DATASET="pumsb_star"
        k=665683
        ;;
    19)
        ALG="radix-SN-BU"
        DATASET="artificial_1"
        k=13255
        ;;
    
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | K=$k"

python3 TopKMiner.py --alg "$ALG" --data "$DATASET" --k "$k" --benchmark

echo "Finished"