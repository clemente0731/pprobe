import time
import functools
from pprobe.utils.logging import Logger

func_counts = 0


def func_torch_step_count_wrapper(func):
    ###################################################
    # torch.autograd.backward / torch.Tensor.backward
    ###################################################
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global func_counts

        if callable(func):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            func_counts += 1
            Logger.info(f"[PPROBE] func_name {func} --> counts {func_counts}")
            return result
        else:
            # handle the case where func is not callable
            Logger.warn(f"func:{func} is not callable")

    return wrapper
