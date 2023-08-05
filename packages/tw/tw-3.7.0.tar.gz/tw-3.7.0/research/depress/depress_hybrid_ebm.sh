#!/bin/bash

TASK=$1
DATASET=AVEC2014
MODEL=i3d
DEVICE=cuda:0

if [[ "$DATASET" = "AVEC2014" ]]; then
DATASET_TRAIN=_datasets/depression/AVEC2014/pp_trn.txt
DATASET_TEST=_datasets/depression/AVEC2014/pp_tst.txt
elif [[ "$DATASET" = "AVEC2013" ]]; then
DATASET_TRAIN=_datasets/depression/AVEC2013/pp_trn.txt
DATASET_TEST=_datasets/depression/AVEC2014/pp_tst.txt
fi

if [[ "$TASK" = "train" ]]; then

python depress_hybrid_ebm.py \
  --name DepressHybridEBM.$MODEL \
  --device $DEVICE \
  --task train \
  --model-name $MODEL \
  --train-lr 0.0001 \
  --train-batchsize 8 \
  --train-epoch 240 \
  --train-dataset $DATASET_TRAIN \
  --test-dataset $DATASET_TEST \
  --test-batchsize 8 \
  --model-source vanilla \
  --model-path _outputs/Depress3D.i3d.210809181715/model.epoch-155.step-64000.pth

elif [[ "$TASK" = "viz" ]]; then

echo "NotImplementedError"

elif [[ "$TASK" = "test" ]]; then

python depress_hybrid_ebm.py \
  --name DepressHybridEBM.$MODEL \
  --device $DEVICE \
  --task test \
  --model-name $MODEL \
  --test-dataset $DATASET_TEST \
  --test-batchsize 8

fi
