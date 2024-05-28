#!/bin/bash
set -euo pipefail

# 获取项目根目录
project_dir=$(git rev-parse --show-toplevel)

# 切换到项目根目录
cd "${project_dir}"

cd pprobe/tests

time python xtest_torchvision_model_mini_ctx.py -a resnet50 --epochs 1 -b 12 -p 1 --seed 42 --dummy
# time python xtest_torchvision_model_normal_ctx.py -a resnet50 --epochs 1 -b 12 -p 1 --seed 42 --dummy
