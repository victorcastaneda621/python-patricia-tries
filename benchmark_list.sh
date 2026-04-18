#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 48:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-1

mkdir -p logs

ALG="list"

case $SLURM_ARRAY_TASK_ID in
    0)
        ALG="list"
        DATASET="mushroom"
        MINSUP=640
        ;;
    1)
        ALG="list"
        DATASET="connect4"
        MINSUP=40535
        ;;
    2)
        ALG="list"
        DATASET="pumsb"
        MINSUP=35000
        ;;
    3)
        ALG="list"
        DATASET="pumsb_star"
        MINSUP=14000
        ;;
    4)
        ALG="list"
        DATASET="artificial_1"
        MINSUP=200
        ;;
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" --benchmark

echo "Finished"