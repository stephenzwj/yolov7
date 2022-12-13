python train.py \
    --weights weights/yolov7x_training.pt \
    --cfg cfg/training/yolov7x_IDID.yaml \
    --data data/voc_IDID.yaml  \
    --device 0 \
    --epochs 1 --batch-size 32 --img-size 640 \
    --save_period 50\
    --nosave \
    --cache-images