import torch
import torch.nn as nn

# Create a tensor on GPU
tensor = torch.randn(3, 3).cuda()

# Create a model on GPU
model = nn.Linear(3, 3).cuda()

# Method 1: Using tensor.to("cpu")
tensor_to_cpu_1 = tensor.to("cpu")

# Method 2: Using tensor.to(torch.device("cpu"))
tensor_to_cpu_2 = tensor.to(torch.device("cpu"))

# Method 3: Using tensor.cpu()
tensor_to_cpu_3 = tensor.cpu()

# Method 1: Using model.to("cpu")
model_to_cpu_1 = model.to("cpu")

# Method 2: Using model.to(torch.device("cpu"))
model_to_cpu_2 = model.to(torch.device("cpu"))

# Method 3: Using model.cpu()
model_to_cpu_3 = model.cpu()