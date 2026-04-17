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

case $SLURM_ARRAY_TASK_ID in
    0)
        ALG="radix-MN-TD"
        DATASET="artificial_1"
        MINSUP=200
        ;;
    1)
        ALG="radix-SN-TD"
        DATASET="artificial_1"
        MINSUP=200
        ;;
    
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP"

echo "Finished"