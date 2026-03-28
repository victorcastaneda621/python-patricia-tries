#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 15:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-9

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    0)
        ALG="radix-single-node"
        DATASET="mushroom"
        MINSUP=640
        ;;
    1)
        ALG="radix-single-node"
        DATASET="connect4"
        MINSUP=40535
        ;;
    2)
        ALG="radix-single-node"
        DATASET="pumsb"
        MINSUP=29400
        ;;
    3)
        ALG="radix-single-node"
        DATASET="pumsb_star"
        MINSUP=9810
        ;;
    4)
        ALG="radix-single-node"
        DATASET="artificial_1"
        MINSUP=200
        ;;
    5)
        ALG="radix-multi-node"
        DATASET="mushroom"
        MINSUP=640
        ;;
    6)
        ALG="radix-multi-node"
        DATASET="connect4"
        MINSUP=40535
        ;;
    7)
        ALG="radix-multi-node"
        DATASET="pumsb"
        MINSUP=29400
        ;;
    8)
        ALG="radix-multi-node"
        DATASET="pumsb_star"
        MINSUP=9810
        ;;
    9)
        ALG="radix-multi-node"
        DATASET="artificial_1"
        MINSUP=200
        ;;
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" --benchmark

echo "Finished"