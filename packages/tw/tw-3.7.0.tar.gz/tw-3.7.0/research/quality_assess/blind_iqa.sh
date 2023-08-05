#!/bin/bash

TASK=$1
DATASET=SPAQ
MODEL=attributenet
DEVICE=cuda:0

if [[ "$TASK" = "train" ]]; then

    python blind_iqa.py \
        --name NRIQA.$MODEL.$DATASET \
        --device $DEVICE \
        --task train \
        --dataset $DATASET \
        --train-batchsize 16 \
        --log-val 1 \
        --log-save 1 \
        --train-epoch 60 \
        --model $MODEL \
        --input-colorspace RGB

elif [[ "$TASK" = "test" ]]; then

    python blind_iqa.py \
        --name NRIQA.$MODEL.$DATASET \
        --device $DEVICE \
        --task test \
        --dataset $DATASET \
        --model $MODEL \
        --input-colorspace RGB \
        --model-source vanilla \
        --model-path _outputs/NRIQA.patchiqa.mobilenet_v2.roi.FLIVE.210721171905/model.epoch-12.step-22680.pth

elif [[ "$TASK" = "val" ]]; then

    python blind_iqa.py \
        --name NRIQA.$MODEL.$DATASET \
        --device $DEVICE \
        --task val \
        --dataset $DATASET \
        --model $MODEL \
        --model-source vanilla \
        --model-path _outputs/NRIQA.vqa_v3p.SPAQ.211102001331/model.epoch-31.step-17670.pth \
        --input-colorspace RGB

elif [[ "$TASK" = "viz" ]]; then

    python blind_iqa.py \
        --name NRIQA.$MODEL.$DATASET.VIZ \
        --device $DEVICE \
        --task viz \
        --model $MODEL \
        --model-source vanilla \
        --model-path _archive/NRIQA.koncept.mobilenet_v2.KonIQ10k.vanilla/model.epoch-60.step-15060.pth \
        --input-colorspace RGB \
        --viz-input /cephFS/sunmanchin/data/vqa/BigoVqaIIdata_Clips/png//0/6839798145093845833_0/0120/00000003.png \
        --viz-output _demo

elif [[ "$TASK" = "onnx" ]]; then

    python blind_iqa.py \
        --name NRIQA.$MODEL.$DATASET.ONNX \
        --device $DEVICE \
        --task onnx \
        --model $MODEL \
        --model-source vanilla \
        --model-path _checkpoints/quality_assess/vqa_v3/vqa_v3_multihead_0928.pth \
        --input-colorspace RGB

fi
