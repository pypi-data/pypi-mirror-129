#!/bin/bash

TASK=$1
DATASET=CSIQ
MODEL=psnr

if [[ "$TASK" = "val" ]]; then

python full_reference_iqa.py \
    --name FRIQA.$MODEL.$DATASET \
    --device cuda:0 \
    --task val \
    --dataset $DATASET \
    --repeat 25 \
    --model $MODEL \
    --input-colorspace RGB

fi