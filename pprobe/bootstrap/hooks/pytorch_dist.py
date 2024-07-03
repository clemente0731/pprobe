import time
import functools
from pprobe.utils.logging import Logger


def func_torch_distributed_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if callable(func):
            result = func(*args, **kwargs)
            # TODO: Refine the handling of each function.
            if isinstance(args, tuple):
                Logger.info(f"[PPROBE] torch.distributed.{func.__qualname__}")
            else:
                Logger.info(f"[PPROBE] torch.distributed.{func.__qualname__}")
            return result
        else:
            # handle the case where func is not callable
            Logger.warn(f"[PPROBE] func:{func} is not callable")

    return wrapper
