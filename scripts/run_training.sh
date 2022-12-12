python train.py \
    --weights weights/yolov7x_training.pt \
    --cfg cfg/training/yolov7x_IDID.yaml \
    --data data/voc_IDID.yaml  \
    --device 0 \
    --epochs 200 --batch-size 24 --img-size 640 \
    --save_period 50\
    --cache-images