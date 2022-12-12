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

image="/hpctmp/zwj/SIF/cv-v0.1.sif"
find /hpctmp/zwj/ -type f -exec touch -am {} \;
singularity exec -e $image bash << EOF > hpc_outputs/out-$PBS_JOBID.txt
./scripts/run_training.sh
EOF