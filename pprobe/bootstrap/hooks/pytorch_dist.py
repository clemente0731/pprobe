import time
import functools
from pprobe.utils.logging import Logger

"""
shape: val.shape
dtype: val.dtype
mean: val.mean().item()
std: val.mean().item()
"""


def func_torch_distributed_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if callable(func):
            result = func(*args, **kwargs)
            if func.__module__ == "torch.distributed" and func.__name__ == "all_gather":
                print("xxxxxxx", func)
            if isinstance(args, tuple):
                Logger.info(f"[PPROBE] torch.distributed.{func.__qualname__}")
            else:
                Logger.info(f"[PPROBE] torch.distributed.{func.__qualname__}")
            return result
        else:
            # handle the case where func is not callable
            Logger.warn(f"[PPROBE] func:{func} is not callable")

    return wrapper
