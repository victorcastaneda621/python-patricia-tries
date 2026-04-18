#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 24:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-5

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    0)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        MINSUP=650
        ;;
    1)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        MINSUP=550
        ;;
    2)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        MINSUP=450
        ;;
    3)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        MINSUP=350
        ;;
    4)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        MINSUP=250
        ;;
    5)
        ALG="radix-SN-TD"
        DATASET="mushroom"
        MINSUP=150
        ;;
    
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" --benchmark

echo "Finished"