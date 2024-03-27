import functools
import importlib
import sys
import time

_hook_modules = {'hello_torch'}


class MetaPathFinder:

    def find_module(self, fullname, path=None):
        print('find_module {}'.format(fullname))
        if fullname in _hook_modules:
            return MetaPathLoader()


class MetaPathLoader:

    def load_module(self, fullname):
        print('load_module {}'.format(fullname))
        # ``sys.modules`` 中保存的是已经导入过的 module
        if fullname in sys.modules:
            return sys.modules[fullname]

        # 先从 sys.meta_path 中删除自定义的 finder
        # 防止下面执行 import_module 的时候再次触发此 finder
        # 从而出现递归调用的问题
        finder = sys.meta_path.pop(0)
        # 导入 module
        module = importlib.import_module(fullname)

        module_hook(fullname, module)

        sys.meta_path.insert(0, finder)
        return module

sys.meta_path.insert(0, MetaPathFinder())


def module_hook(fullname, module):
    if fullname == 'hello_torch':
        # monkey-patch 
        # 这里把 torch.add替换成torch.sub
        module.torch_add = func_wrapper(module.torch_sub)


def func_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("开始函数 == func")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("结束函数 == func")
        print("花费时间 {}s".format(end - start))
        return result
    return wrapper