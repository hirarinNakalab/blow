#!/bin/bash

for SPLIT in train+valid test
do
echo $SPLIT
python synthesize.py --base_fn_model ../res/model/blow --path_out ../res/audio/ --convert --split $SPLIT --force_source_speaker noised --force_target_speaker raw
done
