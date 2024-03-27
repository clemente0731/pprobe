import sys
import hello_torch
import torch

# torch.add 替换为 torch.sub
print(sys.argv)
tensor1 = torch.tensor([1, 2, 3])
tensor2 = torch.tensor([4, 5, 6])
print(f"tensor1:{tensor1} + tensor2:{tensor2}")
print(hello_torch.torch_add(tensor1, tensor2))