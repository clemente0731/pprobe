import time
import functools
from pprobe.utils.logging import Logger
from typing import Any, Callable

func_counts = 0


def func_torch_step_count_wrapper(func):
    """
    torch.autograd.backward / torch.Tensor.backward
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global func_counts

        if callable(func):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            func_counts += 1
            Logger.info(f"[PPROBE] training func_name {func} --> counts {func_counts}")
            return result
        else:
            # handle the case where func is not callable
            Logger.warn(f"func:{func} is not callable")

    return wrapper


def dataloader_next_method_wrapper(original_next: Callable) -> Callable:
    """
    Decorator function to wrap the original __next__ method and add additional debug information.
    """

    def wrapper(self) -> Any:
        iter_count = self._num_yielded + 1
        Logger.info(f"[PPROBE] Iteration count ===>:{iter_count}")
        return original_next(self)

    return wrapper
