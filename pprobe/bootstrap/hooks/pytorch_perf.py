import time
import functools
from pprobe.utils.logging import Logger


def func_torch_device_conversion_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if callable(func):
            tensor_ret = func(*args, **kwargs)

            if func.__name__ == "to":
                Logger.warn(
                    f"[PPROBE] find device conversion call {func}, The tensor is conversion to {str(tensor_ret.device)}"
                )
            elif func.__name__ == "cpu":
                Logger.warn(
                    f"[PPROBE] find device conversion call {func}, The tensor is on CPU"
                )
            elif func.__name__ == "cuda":
                Logger.info(
                    f"[PPROBE] find device conversion call {func}, The tensor is on {str(tensor_ret.device)}"
                )

            return tensor_ret
        else:
            # handle the case where func is not callable
            Logger.warn(f"func:{func} is not callable")

    return wrapper
