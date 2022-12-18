#!/bin/bash

# Set default value for device_count if it is not provided
device_count=''

# Parse command-line arguments using getopts
while getopts ":d:" opt; do
  case $opt in
    d) device_count="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2;;
  esac
done

# Check if device_count is a number
if [[ $device_count =~ ^[0-9]+$ ]]; then
  # Generate the string
  string=""
  for ((i=0;i<$device_count;i++)); do
    string="$string,$i"
  done

  # get the string
  devices="${string:1}"
  batch_size=$((32*$device_count))
else
  # Set devices to device_count
  devices="$device_count"
  batch_size=32
fi
echo "Running with devices $devices and batch_size $batch_size"

python train.py \
    --weights weights/yolov7x_training.pt \
    --cfg cfg/training/yolov7x_IDID.yaml \
    --data data/voc_IDID.yaml  \
    --device $device \
    --epochs 200 --batch-size $batch_size --img-size 640 \
    --save_period 50\
    --nosave \
    --cache-images
