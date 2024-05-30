import time
import functools
import traceback
from .logging import Logger

func_counts = 0


def trace_function_call():
    try:
        raise Exception("Trace function call")
    except:
        # 获取调用堆栈信息
        stack_trace = traceback.extract_stack()
        # 打印堆栈信息
        for stack_entry in stack_trace[:-2]:
            Logger.warn(f"\t\t Trace File: {stack_entry.filename}, Line: {stack_entry.lineno}")


def func_torch_step_count_wrapper(func):
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

def func_torch_device_conversion_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if callable(func):
            tensor_ret = func(*args, **kwargs)

            if func.__name__ == "to":
                trace_function_call()
                Logger.warn(f"[PPROBE] find device conversion call {func}, The tensor is conversion to {str(tensor_ret.device)}")
            elif func.__name__ == "cpu":
                trace_function_call()
                Logger.warn(f"[PPROBE] find device conversion call {func}, The tensor is on CPU")
            elif func.__name__ == "cuda":
                Logger.info(f"[PPROBE] find device conversion call {func}, The tensor is on {str(tensor_ret.device)}")

            return tensor_ret
        else:
            # handle the case where func is not callable
            Logger.warn(f"func:{func} is not callable")
    return wrapper

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
            Logger.warn(f"func:{func} is not callable")
    return wrapper

def torch_hook_fn(fullname, module):
    if fullname == "torch":
        ###################################################
        # torch.autograd.backward / torch.Tensor.backward 
        ###################################################
        module.autograd.backward = func_torch_step_count_wrapper(module.autograd.backward)

        ###################################################
        ## torch.distributed part
        ###################################################
        module.distributed.broadcast = func_torch_distributed_wrapper(module.distributed.broadcast)
        module.distributed.all_reduce = func_torch_distributed_wrapper(module.distributed.all_reduce)
        module.distributed.reduce = func_torch_distributed_wrapper(module.distributed.reduce)
        module.distributed.all_gather = func_torch_distributed_wrapper(module.distributed.all_gather)
        module.distributed.gather = func_torch_distributed_wrapper(module.distributed.gather)
        module.distributed.scatter = func_torch_distributed_wrapper(module.distributed.scatter)
        module.distributed.reduce_scatter = func_torch_distributed_wrapper(module.distributed.reduce_scatter)
        module.distributed.send = func_torch_distributed_wrapper(module.distributed.send)
        module.distributed.recv = func_torch_distributed_wrapper(module.distributed.recv)
        module.distributed.barrier = func_torch_distributed_wrapper(module.distributed.barrier)

        ###################################################
        ## torch.Tensor.to part
        ###################################################
        module.Tensor.to = func_torch_device_conversion_wrapper(module.Tensor.to)
        module.Tensor.cpu = func_torch_device_conversion_wrapper(module.Tensor.cpu)
        module.Tensor.cuda = func_torch_device_conversion_wrapper(module.Tensor.cuda)