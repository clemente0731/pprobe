import torch
import torch.nn.functional as F
import numpy as np
import csv
from datetime import datetime
import time
import os
import torch.distributed as dist
from torch.overrides import TorchFunctionMode, resolve_name, is_tensor_like

class TorchFunctioContext(TorchFunctionMode):
    def __init__(self):
        super().__init__()
        self.func_idx = 0

        self.filename = self.generate_filename()

        # 初始化 CSV 文件并写入标题行
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Function", "Metadata_args_1", "Metadata_args_2", "Metadata_args_3", "Metadata_args_4", "Metadata_args_5", "Metadata_args_6", "Metadata_args_7", "Metadata_args_8", "Kwargs", "Types", "Raw_Function"])


    def get_tensors_metadata(self, func_args):
        meta_list = []
        if isinstance(func_args, tuple):
            for idx, tensor in enumerate(func_args):
                if isinstance(tensor, torch.Tensor):
                    # 求平均值 解决long类型的报错 需要提前转成 float
                    mean_value = torch.mean(tensor.float()).item()
                    # 求标准差 解决long类型的报错 需要提前转成 float
                    std_dev = torch.std(tensor.float()).item()
                    # 获取dtype
                    dtype = tensor.dtype
                    # 获取形状
                    shape = tensor.shape
                    # 构造元数据字典
                    meta = {
                        "args_idx": idx,
                        "Mean": mean_value,
                        "Standard Deviation": std_dev,
                        "Dtype": dtype,
                        "Shape": shape,
                        "TensorOrNot": True
                    }
                    meta_list.append(meta)

                if isinstance(tensor, (int, float, bool)):
                    meta = {
                        "args_idx": idx,
                        "Mean": tensor,
                        "Standard Deviation": np.std([tensor]),
                        "Dtype": type(tensor),
                        "Shape": 1,
                        "TensorOrNot": False
                    }
                    meta_list.append(meta)
        # print(f"tensors_metadata: {meta_list}")
        return meta_list

    def generate_filename(self):
        # 获取当前日期和时间
        now = datetime.now()
        # 格式化日期和时间字符串
        timestamp = now.strftime("%Y%m%d%H%M")
        # 构建文件名
        filename = f"{timestamp}_function_dump.csv"
        return filename

    def fill_missing_values(self, meta):
        # 如果 meta 的长度小于 8，则填充 "NA"，使其长度为 8
        while len(meta) < 8:
            meta.append("NA")
        return meta


    def __torch_function__(self, func, types, args, kwargs=None):
        # 打印 torch module接口
        self.func_idx += 1
        meta = self.get_tensors_metadata(args)
        meta = self.fill_missing_values(meta)
        # 填充缺失值
        #print(f"[PYTORCH FUNCTION]: idx:{self.func_idx}, func_name:{resolve_name(func)}, meta:{meta}, kwargs: {kwargs} , types: {types}, raw_func: {func} \n",  flush=True)

        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.func_idx, resolve_name(func), meta[0], meta[1], meta[2], meta[3],meta[4],meta[5],meta[6],meta[7], kwargs, types, func])

        out = func(*args, **(kwargs or {}))
        # get_tensors_metadata(args)
        # print(f"{resolve_name(func)}(*{args}, **{kwargs})", flush=True)
        return out



# context = TorchFunctioContext()
# context.__enter__()