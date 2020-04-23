#!/bin/bash

cd src
python synthesize.py --base_fn_model ../res/model/blow --path_out ../res/audio/ --convert --split train+valid --force_source_speaker noised --force_target_speaker raw
python synthesize.py --base_fn_model ../res/model/blow --path_out ../res/audio/ --convert --split test --force_source_speaker noised --force_target_speaker raw
