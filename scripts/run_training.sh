python train.py \
    --weights weights/yolov7x_training.pt \
    --cfg cfg/training/yolov7x_insul.yaml  --data data/voc_insul.yaml  --device 0 --epochs 100 --batch-size 8 --img-size 640