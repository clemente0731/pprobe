import importlib
import sys
from .logging import Logger
from .pt_specific_hook import torch_hook_fn

_hook_modules = {'torch'}


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
        torch_hook_fn(fullname, module)
        sys.meta_path.insert(0, finder)

        return module

sys.meta_path.insert(0, MetaPathFinder())
