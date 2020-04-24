#!/bin/bash

mkdir ../22.05k
find . -name "*.wav" -exec sox {} -r 22050 ../22.05k/{} \;