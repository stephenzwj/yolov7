#!/bin/bash
#PBS -P Project
#PBS -j oe
#PBS -N yolov7
#PBS -q volta_gpu
#PBS -l select=1:ncpus=10:mem=32gb:ngpus=1
#PBS -l walltime=12:00:00

cd $PBS_O_WORKDIR;
echo "Running on dir ${PBS_O_WORKDIR}";
np=$(cat ${PBS_NODEFILE} | wc -l);
find /hpctmp/zwj/ -type f -exec touch -am {} \;
image="/hpctmp/zwj/SIF/cv-v0.1.sif"
singularity exec -e $image bash ./scripts/get_command_outputs.sh "./scripts/run_training.sh" > hpc_outputs/out-$PBS_JOBID.txt 2>&1;