#!/bin/bash
#PBS -P Project
#PBS -j oe
#PBS -N yolov7
#PBS -q volta_gpu
#PBS -l select=1:ncpus=10:mem=32gb:ngpus=1
#PBS -l walltime=12:00:00

cd $PBS_o_WORKDIR;
echo "Running on dir ${PBS_o_WORKDIR}";
np=$(cat ${PBS_NODEFILE} | wc -l);

image="/home/svu/zwj/SIF/cv-v0.1.sif"
singularity exec -e $image bash << EOF > stdout.$PBS_JOBID 2> stderr.$PBS_JOBID
./scripts/run_training.sh
EOF