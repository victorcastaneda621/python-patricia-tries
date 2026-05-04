#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 48:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-4

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    0)
        ALG="patricia"
        DATASET="mushroom"
        k=915325
        ;;
    1)
        ALG="patricia"
        DATASET="connect4"
        k=8368159
        ;;
    2)
        ALG="patricia"
        DATASET="pumsb"
        k=1897479
        ;;
    3)
        ALG="patricia"
        DATASET="pumsb_star"
        k=665683
        ;;
    4)
        ALG="patricia"
        DATASET="artificial_1"
        k=13255
        ;;
    
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | K=$k"

python3 TopKMiner.py --alg "$ALG" --data "$DATASET" --k "$k" --benchmark

echo "Finished"