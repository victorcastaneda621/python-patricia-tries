#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 00:30:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-3

mkdir -p logs

ALG="list"
MINSUP=1

datasets=(
    "mushroom"
    "connect4"
    "pumsb"
    "artificial_1"
    "kosarak"
    "pumsb_star"
)

DATASET=${datasets[$SLURM_ARRAY_TASK_ID]}

echo "Starting: Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" --benchmark

echo "Finished"