import os
import time
import csv

from datetime import datetime
import numpy as np
import torch
import torch.nn.functional as F
import torch.distributed as dist
from torch.overrides import TorchFunctionMode, resolve_name, is_tensor_like
import torch.distributed as dist


class TorchFunctionContext(TorchFunctionMode):
    """
    USAGE:


    from pprobe.bootstrap import torchfunc_hook
    context=torchfunc_hook.TorchFunctionContext()
    context.__enter__()

    # Place the code block that needs to be managed here. like:
    import torch
    a = torch.tensor([1, 2, 3], dtype=torch.float32)
    b = torch.tensor([4, 5, 6], dtype=torch.float32)
    c = a + b


    context.__exit__()
    """
    def __init__(self):
        super().__init__()
        self.func_idx = 0

        self.filename = self.generate_filename()

        # 初始化 CSV 文件并写入标题行
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Index",
                    "Function",
                    "Metadata_args_1",
                    "Metadata_args_2",
                    "Metadata_args_3",
                    "Metadata_args_4",
                    "Metadata_args_5",
                    "Metadata_args_6",
                    "Metadata_args_7",
                    "Metadata_args_8",
                    "Metadata_output",
                    "Kwargs",
                    "Types",
                    "Raw_Function",
                ]
            )

    def is_multi_gpu_multi_rank(self):
        # Get the number of available GPUs
        num_gpus = torch.cuda.device_count()

        # Check if multiple GPUs are available
        if num_gpus > 1:
            # Check if distributed training is enabled
            if dist.is_available() and dist.is_initialized():
                print(f"Detected {num_gpus} GPUs in multi-GPU multi-rank setup.")
                return True
        print(f"Detected {num_gpus} GPU(s) in single-GPU setup.")
        return False

    def get_input_metadata(self, func_args):
        meta_list = []

        if isinstance(func_args, tuple):
            for idx, tensor in enumerate(func_args):
                meta = {"args_idx": idx}  # Initialize the meta dictionary

                if isinstance(tensor, torch.Tensor):
                    mean_value = torch.mean(tensor.float()).item()
                    std_dev = torch.std(tensor.float()).item()
                    dtype = tensor.dtype
                    shape = tensor.shape

                    # Assign values to meta dictionary keys
                    meta["input_mean"] = mean_value
                    meta["input_std"] = std_dev
                    meta["input_dtype"] = dtype
                    meta["input_shape"] = shape
                    meta["input_tensor_or_not"] = True

                if isinstance(tensor, (int, float, bool)):
                    # Assign values to meta dictionary keys
                    meta["input_mean"] = tensor
                    meta["input_std"] = np.std([tensor])
                    meta["input_dtype"] = type(tensor)
                    meta["input_shape"] = 1
                    meta["input_tensor_or_not"] = False

                meta_list.append(meta)

        return meta_list

    def get_output_metadata(self, output_val):
        output_meta = {}

        if isinstance(output_val, torch.Tensor):
            output_val_float = output_val.float()
            output_meta["output_mean"] = output_val_float.mean().item()
            output_meta["output_std"] = output_val_float.std().item()
            output_meta["output_dtype"] = output_val.dtype
            output_meta["output_shape"] = output_val.shape
            output_meta["output_tensor_or_not"] = True

        elif isinstance(output_val, (int, float, bool)):
            output_meta["output_mean"] = output_val
            output_meta["output_std"] = np.std([output_val])
            output_meta["output_dtype"] = type(output_val)
            output_meta["output_shape"] = 1
            output_meta["output_tensor_or_not"] = False

        return output_meta

    def generate_filename(self):
        # Get current date and time
        now = datetime.now()

        # Check if it's multi-GPU multi-rank or single-GPU
        if self.is_multi_gpu_multi_rank():
            rank = dist.get_rank()
            filename = f"{now.strftime('%Y%m%d%H%M')}_function_rank_{rank}_dump.csv"
        else:
            filename = f"{now.strftime('%Y%m%d%H%M')}_function_rank_0_dump.csv"

        return filename

    def fill_missing_values(self, meta):
        # 如果 meta 的长度小于 8，则填充 "NA"，使其长度为 8
        while len(meta) < 8:
            meta.append("NA")
        return meta

    def __torch_function__(self, func, types, args, kwargs=None):
        # 打印 torch module接口
        self.func_idx += 1

        output = func(*args, **(kwargs or {}))

        if resolve_name(func) and any(keyword in resolve_name(func) for keyword in ["dtype", "shape"]):
            # If the function name includes "torch.Tensor.dtype" or "torch.Tensor.shape", return the output value directly without further processing
            return output

        # print(f"{resolve_name(func)}() ===== type(output) {type(output)}", flush=True)

        input_meta = self.get_input_metadata(args)
        output_meta = self.get_output_metadata(output)

        input_meta = self.fill_missing_values(input_meta)
        # 填充缺失值
        # print(f"[PYTORCH FUNCTION]: idx:{self.func_idx}, func_name:{resolve_name(func)}, meta:{meta}, kwargs: {kwargs} , types: {types}, raw_func: {func} \n",  flush=True)

        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    self.func_idx,
                    resolve_name(func),
                    input_meta[0],
                    input_meta[1],
                    input_meta[2],
                    input_meta[3],
                    input_meta[4],
                    input_meta[5],
                    input_meta[6],
                    input_meta[7],
                    output_meta,
                    kwargs,
                    types,
                    func,
                ]
            )

        # get_input_metadata(args)
        # print(f"{resolve_name(func)}(*{args}, **{kwargs})", flush=True)
        return output


class TorchFunctionMiniContext(TorchFunctionMode):
    """
    USAGE:


    from pprobe.bootstrap import torchfunc_hook
    context=torchfunc_hook.TorchFunctionMiniContext()
    context.__enter__()

    # Place the code block that needs to be managed here. like:
    import torch
    a = torch.tensor([1, 2, 3], dtype=torch.float32)
    b = torch.tensor([4, 5, 6], dtype=torch.float32)
    c = a + b


    context.__exit__()
    """
    def __init__(self):
        super().__init__()
        self.func_idx = 0

        self.filename = self.generate_filename()

        # 初始化 CSV 文件并写入标题行
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Index",
                    "Function",
                    "Kwargs",
                    "Types",
                    "Raw_Function",
                ]
            )

    def is_multi_gpu_multi_rank(self):
        # Get the number of available GPUs
        num_gpus = torch.cuda.device_count()

        # Check if multiple GPUs are available
        if num_gpus > 1:
            # Check if distributed training is enabled
            if dist.is_available() and dist.is_initialized():
                print(f"Detected {num_gpus} GPUs in multi-GPU multi-rank setup.")
                return True
        print(f"Detected {num_gpus} GPU(s) in single-GPU setup.")
        return False

    def generate_filename(self):
        # Get current date and time
        now = datetime.now()

        # Check if it's multi-GPU multi-rank or single-GPU
        if self.is_multi_gpu_multi_rank():
            rank = dist.get_rank()
            filename = f"{now.strftime('%Y%m%d%H%M')}_mini_function_rank_{rank}_dump.csv"
        else:
            filename = f"{now.strftime('%Y%m%d%H%M')}_mini_function_rank_0_dump.csv"

        return filename

    def fill_missing_values(self, meta):
        # 如果 meta 的长度小于 8，则填充 "NA"，使其长度为 8
        while len(meta) < 8:
            meta.append("NA")
        return meta

    def __torch_function__(self, func, types, args, kwargs=None):
        self.func_idx += 1

        output = func(*args, **(kwargs or {}))


        if resolve_name(func) and any(keyword in resolve_name(func) for keyword in ["dtype", "shape"]):
            # If the function name includes "torch.Tensor.dtype" or "torch.Tensor.shape", return the output value directly without further processing
            return output
    
        print(f"{resolve_name(func)}() ===== type(output) {type(output)}", flush=True)

        # 填充缺失值
        # print(f"[PYTORCH FUNCTION]: idx:{self.func_idx}, func_name:{resolve_name(func)}, meta:{meta}, kwargs: {kwargs} , types: {types}, raw_func: {func} \n",  flush=True)

        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    self.func_idx,
                    resolve_name(func),
                    func,
                ]
            )

        # get_input_metadata(args)
        # print(f"{resolve_name(func)}(*{args}, **{kwargs})", flush=True)
        return output
