import functools
import importlib
import sys
import time
from .logging import Logger
# import torch
_hook_modules = {'torch'}
func_counts = 0

class MetaPathFinder:

    def find_module(self, fullname, path=None):
        # Logger.info('find_module {}'.format(fullname))
        if fullname in _hook_modules:
            return MetaPathLoader()

class MetaPathLoader:

    def load_module(self, fullname):
        # Logger.info('load_module {}'.format(fullname))
        # ``sys.modules`` 中保存的是已经导入过的 module
        if fullname in sys.modules:
            return sys.modules[fullname]

        # 先从 sys.meta_path 中删除自定义的 finder
        # 防止下面执行 import_module 的时候再次触发此 finder
        # 从而出现递归调用的问题
        finder = sys.meta_path.pop(0)
        module = importlib.import_module(fullname)
        Logger.info(f"META-PATH-LOADER --> MODULE {module}")
        module_hook(fullname, module)
        sys.meta_path.insert(0, finder)

        return module

sys.meta_path.insert(0, MetaPathFinder())

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
            # 处理 func 不可调用的情况
            Logger.warn(f"func:{func} is not callable")
    return wrapper

def func_torch_distributed_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if callable(func):
            result = func(*args, **kwargs)
            if isinstance(args, tuple):
                try:
                    args_info = ", ".join([f"args_{idx} shape {arg.shape}, dtype {arg.dtype} " for idx, arg in enumerate(args)])
                    Logger.info(f"[PPROBE] torch.distributed.{func.__qualname__} {args_info}, kwargs {kwargs}")
                except:
                    Logger.warn(f"[PPROBE] torch.distributed.{func.__qualname__} 出错了 需要排查一下\n")
            else:
                Logger.info(f"[PPROBE] torch.distributed.{func.__qualname__} args {args}, kwargs {kwargs} ")
            return result
        else:
            # 处理 func 不可调用的情况
            Logger.warn(f"func:{func} is not callable")
    return wrapper

def module_hook(fullname, module):
    if fullname == "torch":
        # torch.Tensor.backward 和 torch.autograd.backward 是等价的
        module.autograd.backward = func_torch_step_count_wrapper(module.autograd.backward)

        # torch.distributed part
        module.distributed.broadcast = func_torch_distributed_wrapper(module.distributed.broadcast)
        module.distributed.all_reduce = func_torch_distributed_wrapper(module.distributed.all_reduce)
        module.distributed.reduce = func_torch_distributed_wrapper(module.distributed.reduce)
        module.distributed.all_gather = func_torch_distributed_wrapper(module.distributed.all_gather)
        module.distributed.gather = func_torch_distributed_wrapper(module.distributed.gather)
        module.distributed.scatter = func_torch_distributed_wrapper(module.distributed.scatter)
        module.distributed.reduce_scatter = func_torch_distributed_wrapper(module.distributed.reduce_scatter)
        module.distributed.send = func_torch_distributed_wrapper(module.distributed.send)
        module.distributed.recv = func_torch_distributed_wrapper(module.distributed.recv)

        # torch.distributed.broadcast(tensor, src, group=None, async_op=False)
        # torch.distributed.all_reduce(tensor, op=<RedOpType.SUM: 0>, group=None, async_op=False)
        # torch.distributed.reduce(tensor, dst, op=<RedOpType.SUM: 0>, group=None, async_op=False)
        # torch.distributed.all_gather(tensor_list, tensor, group=None, async_op=False)
        # torch.distributed.gather(tensor, gather_list=None, dst=0, group=None, async_op=False)
        # torch.distributed.scatter(tensor, scatter_list=None, src=0, group=None, async_op=False)
        # torch.distributed.reduce_scatter(output, input_list, op=<RedOpType.SUM: 0>, group=None, async_op=False)
        # torch.distributed.send(tensor, dst, group=None, tag=0)
        # torch.distributed.recv(tensor, src=None, group=None, tag=0)
        # torch.distributed.barrier(group=None, async_op=False, device_ids=None)
