import torch
import torch.nn as nn

# 获取可用设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tensor = torch.randn(3, 3).to(device)
model = nn.Linear(3, 3).to(device)

# 将张量移动到 CPU 的三种方法
# Method 1: Using tensor.to("cpu")
tensor_to_cpu_1 = tensor.to("cpu")

# Method 2: Using tensor.to(torch.device("cpu"))
tensor_to_cpu_2 = tensor.to(torch.device("cpu"))

# Method 3: Using tensor.cpu()
tensor_to_cpu_3 = tensor.cpu()

# 将模型移动到 CPU 的三种方法
# Method 1: Using model.to("cpu")
model_to_cpu_1 = model.to("cpu")

# Method 2: Using model.to(torch.device("cpu"))
model_to_cpu_2 = model.to(torch.device("cpu"))

# Method 3: Using model.cpu()
model_to_cpu_3 = model.cpu()

print(f"Using device: {device}")