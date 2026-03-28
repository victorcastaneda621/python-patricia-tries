#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 15:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-2

mkdir -p logs

ALG="list"

case $SLURM_ARRAY_TASK_ID in
    0)
        DATASET="connect4"
        MINSUP=40535
        ;;
    1)
        DATASET="pumsb"
        MINSUP=29400
        ;;
    2)
        DATASET="pumsb_star"
        MINSUP=9810
        ;;
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" --benchmark

echo "Finished"