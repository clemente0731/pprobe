import functools
import importlib
import sys
import time
from .logging import Logger
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

def func_count_wrapper(func):
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

def module_hook(fullname, module):
    if fullname == "torch":
        # torch.Tensor.backward 和 torch.autograd.backward 是等价的
        module.autograd.backward = func_count_wrapper(module.autograd.backward)
