#!/bin/bash

# Set default value for device_count if it is not provided
device_count='cpu'

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
  # if device_count is an empty string, it will be set to "cpu"
  if [ "$device_count" == "" ]; then
    devices="cpu"
  else
    devices="$device_count"
  fi
  batch_size=32
fi

echo "Running tests with devices $devices and batch_size $batch_size"

python test.py \
    --weights runs/train/exp/weights/best.pt \
    --task test \
    --data data/voc_IDID.yaml  \
    --device $devices \
    --batch-size $batch_size --img-size 640 \
    --conf 0.001 \
    --iou 0.65
