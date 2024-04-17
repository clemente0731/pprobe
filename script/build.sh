#!/bin/bash
set -euo pipefail

# 获取项目根目录
project_dir=$(git rev-parse --show-toplevel)

# 切换到项目根目录
cd "${project_dir}"

# 清理项目目录
git clean -dxf

# 构建 wheel 包
python setup.py bdist_wheel

# 打印生成的 wheel 包列表
ls -thl dist
