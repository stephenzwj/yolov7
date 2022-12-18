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
image="/hpctmp/zwj/SIF/cv-pytorch-1.10.0-cuda11.3-cudnn8:v0.1.sif"
num_gpus=$(nvidia-smi -L | wc -l)
echo "Running with $num_gpus GPUs"
singularity exec -e $image bash ./scripts/get_command_outputs.sh "./scripts/run_training.sh -d ${num_gpus}" > hpc_outputs/out-$PBS_JOBID.txt 2>&1;

python train.py \
    --weights weights/yolov7x_training.pt \
    --cfg cfg/training/yolov7x_IDID.yaml \
    --data data/voc_IDID.yaml  \
    --device $devices \
    --epochs 200 --batch-size $batch_size --img-size 640 \
    --save_period 50\
    --cache-images
