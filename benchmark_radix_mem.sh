#!/bin/bash
#SBATCH -J patricia_mine          
#SBATCH -o logs/bench_%A_%a.out   
#SBATCH -e logs/bench_%A_%a.err   
#SBATCH -t 70:00:00               
#SBATCH --mem-per-cpu=4096        
#SBATCH -n 1                      
#SBATCH -c 1
#SBATCH --array=0-3

mkdir -p logs

case $SLURM_ARRAY_TASK_ID in
    # Pumsb* Tasks
    0) ALG="radix-SN-TD"; DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;;
    1) ALG="radix-SN-BU"; DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;;
    2) ALG="radix-MN-TD"; DATASET="pumsb_star"; MINSUP=14000; BENCH="--benchmark" ;;
    3) ALG="radix-MN-BU"; DATASET="pumsb_star"; MINSUP=14000; BENCH=""            ;;

    # T10.I4.D100k Tasks
    4) ALG="radix-SN-TD"; DATASET="T10I4D100k"; MINSUP=200;   BENCH=""            ;;
    5) ALG="radix-MN-TD"; DATASET="T10I4D100k"; MINSUP=200;   BENCH=""            ;;
    6) ALG="radix-MN-TD"; DATASET="T10I4D100k"; MINSUP=200;   BENCH="--benchmark" ;;
esac
# ------------------------------------

echo "Starting: ID=$SLURM_ARRAY_TASK_ID | Algorithm=$ALG | Dataset=$DATASET | Minsup=$MINSUP $BENCH_FLAG"

python3 PatriciaMine.py --alg "$ALG" --data "$DATASET" --minsup "$MINSUP" $BENCH_FLAG

echo "Finished"