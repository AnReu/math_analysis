#!/bin/bash
#SBATCH --time=2:00:00   # walltime
#SBATCH --nodes=1  # number of nodes
#SBATCH --ntasks=1      # limit to one node
#SBATCH --mincpus=1
#SBATCH --partition=haswell  # gpu1 K80 GPUs on Haswell node hpdlf
#SBATCH --cpus-per-task=2  # number of processor cores (i.e. threads)
#SBATCH --mem-per-cpu=27000M
#SBATCH --nodes=1
#SBATCH -J "json_data"   # job name
#SBATCH -o "logs/json_data-%j.out"   # output name
#SBATCH --error="logs/json_data-%j.err"   # error file 
#SBATCH -A p_da_poldata # name of the project
#SBATCH --mail-user=anja.reusch@tu-dresden.de   # email address
#SBATCH --mail-type ALL

cd ..

python3 create_training_data_task1_parts_colbert.py

