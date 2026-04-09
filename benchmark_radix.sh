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
        MINSUP=640
        ;;
    1)
        ALG="radix-MN-TD"
        DATASET="connect4"
        MINSUP=40535
        ;;
    2)
        ALG="radix-MN-TD"
        DATASET="pumsb"
        MINSUP=35000
        ;;
    3)
        ALG="radix-MN-TD"
        DATASET="pumsb_star"
        MINSUP=14000
        ;;
    4)
        ALG="radix-MN-TD"
        DATASET="artificial_1"
        MINSUP=200
        ;;
    5)
        ALG="radix-MN-BU"
        DATASET="mushroom"
        MINSUP=640
        ;;
    6)
        ALG="radix-MN-BU"
        DATASET="connect4"
        MINSUP=40535
        ;;
    7)
        ALG="radix-MN-BU"
        DATASET="pumsb"
        MINSUP=35000
        ;;
    8)
        ALG="radix-MN-BU"
        DATASET="pumsb_star"
        MINSUP=14000
        ;;
    9)
        ALG="radix-MN-BU"
        DATASET="artificial_1"
        MINSUP=200
        ;;
    10)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        MINSUP=640
        ;;
    11)
        ALG="radix-SN-TD"
        DATASET="connect4"
        MINSUP=40535
        ;;
    12)
        ALG="radix-SN-TD"
        DATASET="pumsb"
        MINSUP=35000
        ;;
    13)
        ALG="radix-SN-TD"
        DATASET="pumsb_star"
        MINSUP=14000
        ;;
    14)
        ALG="radix-SN-TD"
        DATASET="artificial_1"
        MINSUP=200
        ;;
    15)
        ALG="radix-SN-BU"
        DATASET="mushroom"
        MINSUP=640
        ;;
    16)
        ALG="radix-SN-BU"
        DATASET="connect4"
        MINSUP=40535
        ;;
    17)
        ALG="radix-SN-BU"
        DATASET="pumsb"
        MINSUP=35000
        ;;
    18)
        ALG="radix-SN-BU"
        DATASET="pumsb_star"
        MINSUP=14000
        ;;
    19)
        ALG="radix-SN-BU"
        DATASET="artificial_1"
        MINSUP=200
        ;;
    
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" --benchmark

echo "Finished"