#!/bin/bash
set -euo pipefail

# 获取项目根目录
project_dir=$(git rev-parse --show-toplevel)

# 切换到项目根目录
cd "${project_dir}"

cd pprobe/tests

PPROBE --enable PPROBE_ENABLE
PPROBE --enable TORCH_DUMP_MODULE
PPROBE --enable TORCH_CATCH_STEP
PPROBE --enable TORCH_CATCH_LR

PPROBE_ENABLE=1 python xtest_torchvision_model.py -a resnet50 --epochs 1 -b 12 -p 1 --seed 42 --dummy 
PPROBE_ENABLE=1 python xtest_torchvision_model.py -a resnet50 --epochs 1 -b 12 -p 1 --seed 42 --dummy --evaluate
PPROBE_ENABLE=1 python xtest_device_conversion_detection.py

PPROBE --reset