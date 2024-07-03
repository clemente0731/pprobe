import importlib
import sys
from pprobe.utils.logging import Logger
from pprobe.toggle.cli import ToggleManager

from pprobe.bootstrap.hooks.pytorch_catch import func_torch_step_count_wrapper
from pprobe.bootstrap.hooks.pytorch_perf import func_torch_device_conversion_wrapper


_hook_modules = {"torch"}


class PProbeSetup:
    def __init__(self, module, module_fullname):
        self.module = module
        self.pprobe_toggle = ToggleManager()
        ####################
        ### ENABLE FIELD
        ####################
        self.pprobe_enabled = self.pprobe_toggle.get_toggle("PPROBE_ENABLE")
        self.torch_reproduce_enabled = self.pprobe_toggle.get_toggle("TORCH_REPRODUCE")

        self.torch_catch_step_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_CATCH_STEP"
        )
        self.torch_catch_loss_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_CATCH_LOSS"
        )
        self.torch_catch_lr_enabled = self.pprobe_toggle.get_toggle("TORCH_CATCH_LR")

        self.torch_dump_op_enabled = self.pprobe_toggle.get_toggle("TORCH_DUMP_OP")
        self.torch_dump_dist_enabled = self.pprobe_toggle.get_toggle("TORCH_DUMP_DIST")
        self.torch_dump_module_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_DUMP_MODULE"
        )
        self.torch_dump_optim_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_DUMP_OPTIM"
        )
        self.torch_dump_memory_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_DUMP_MEMORY"
        )
        self.torch_test_dump_op_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_TEST_DUMP_OP"
        )
        self.torch_test_dump_dist_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_TEST_DUMP_DIST"
        )
        self.torch_test_dump_module_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_TEST_DUMP_MODULE"
        )
        self.torch_perf_issue_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_PERF_ISSUE"
        )
        self.torch_torch_trace_file_enabled = self.pprobe_toggle.get_toggle(
            "TORCH_TRACE_FILE"
        )
        ####################
        ### INIT HOOK
        ####################
        self.check_and_run_hook(module_fullname)

    def check_and_run_hook(self, module_fullname):
        if self.pprobe_enabled:
            self.run_generic_hook()
            # torch part
            if module_fullname == "torch":
                if self.torch_reproduce_enabled:
                    # TODO
                    pass
                if self.torch_catch_step_enabled:
                    self.run_torch_catch_step_hook()
                if self.torch_catch_loss_enabled:
                    # TODO
                    pass
                if self.torch_catch_lr_enabled:
                    # TODO
                    pass
                if self.torch_dump_op_enabled:
                    self.run_torch_func_hook()
                if self.torch_dump_dist_enabled:
                    # TODO
                    pass
                if self.torch_dump_module_enabled:
                    self.run_torch_module_hook()
                if self.torch_dump_optim_enabled:
                    # TODO
                    pass
                if self.torch_dump_memory_enabled:
                    # TODO
                    pass
                if self.torch_test_dump_op_enabled:
                    # TODO
                    pass
                if self.torch_test_dump_dist_enabled:
                    # TODO
                    pass
                if self.torch_test_dump_module_enabled:
                    # TODO
                    pass
                if self.torch_perf_issue_enabled:
                    # TODO
                    pass
                if self.torch_torch_trace_file_enabled:
                    # TODO
                    pass
        else:
            self.print_warning()

    def run_generic_hook(self):
        """
        place_holder
        """
        pass

    def run_torch_func_hook(self):
        from pprobe.bootstrap.hooks import pytorch_func_op

        Logger.info(f"[PPROBE] torch function hook executed")
        context = pytorch_func_op.TorchFunctionContext()
        context.__enter__()

    def run_torch_module_hook(self):
        from pprobe.bootstrap.hooks import pytorch_module

        Logger.info(f"[PPROBE] torch module hook executed")

        context = pytorch_module.TorchModuleContext()
        context.__enter__()

    def run_torch_dist_hook(self):
        from pprobe.bootstrap.hooks.pytorch_dist import func_torch_distributed_wrapper

        Logger.info(f"[PPROBE] torch dist hook executed")

        ###################################################
        ## torch.distributed part
        ###################################################
        self.module.distributed.broadcast = func_torch_distributed_wrapper(
            self.module.distributed.broadcast
        )
        self.module.distributed.all_reduce = func_torch_distributed_wrapper(
            self.module.distributed.all_reduce
        )
        self.module.distributed.reduce = func_torch_distributed_wrapper(
            self.module.distributed.reduce
        )
        self.module.distributed.all_gather = func_torch_distributed_wrapper(
            self.module.distributed.all_gather
        )
        self.module.distributed.gather = func_torch_distributed_wrapper(
            self.module.distributed.gather
        )
        self.module.distributed.scatter = func_torch_distributed_wrapper(
            self.module.distributed.scatter
        )
        self.module.distributed.reduce_scatter = func_torch_distributed_wrapper(
            self.module.distributed.reduce_scatter
        )
        self.module.distributed.send = func_torch_distributed_wrapper(
            self.module.distributed.send
        )
        self.module.distributed.recv = func_torch_distributed_wrapper(
            self.module.distributed.recv
        )
        self.module.distributed.barrier = func_torch_distributed_wrapper(
            self.module.distributed.barrier
        )

    def run_torch_reproduce_hook(self):
        # Add the logic for torch reproduce hook
        Logger.info(f"[PPROBE] torch reproduce hook executed")

    def run_torch_catch_step_hook(self):
        ###################################################
        # torch.autograd.backward / torch.Tensor.backward
        ###################################################
        # Add the logic for torch catch_step hook
        Logger.info(f"[PPROBE] torch catch step hook executed")
        self.module.autograd.backward = func_torch_step_count_wrapper(
            self.module.autograd.backward
        )

    def run_torch_perf_hook(self):
        Logger.info(f"[PPROBE] torch perf hook executed")

        ###################################################
        ## torch.Tensor.to part
        ###################################################
        self.module.Tensor.to = func_torch_device_conversion_wrapper(
            self.module.Tensor.to
        )
        self.module.Tensor.cpu = func_torch_device_conversion_wrapper(
            self.module.Tensor.cpu
        )
        self.module.Tensor.cuda = func_torch_device_conversion_wrapper(
            self.module.Tensor.cuda
        )

    def print_warning(self):
        if not getattr(self, "warning_printed", False):
            print(
                "[PPROBE] Please set the environment variable PPROBE_ENABLE=1 to use pprobe."
            )
            setattr(self, "warning_printed", True)


class MetaPathFinder:
    def find_module(self, module_fullname, path=None):
        # Logger.info('find_module {}'.format(module_fullname))
        if module_fullname in _hook_modules:
            return MetaPathLoader()


class MetaPathLoader:
    def load_module(self, module_fullname):
        # Logger.info('load_module {}'.format(module_fullname))

        # sys.modules中保存的是已经导入过的 module
        if module_fullname in sys.modules:
            return sys.modules[module_fullname]

        ##################################################
        # 先从 sys.meta_path 中删除自定义的 finder
        # 防止下面执行 import_module 的时候再次触发此 finder
        # 从而出现递归调用的问题
        ##################################################
        finder = sys.meta_path.pop(0)
        module = importlib.import_module(module_fullname)

        # Logger.info(f"META-PATH-LOADER --> MODULE {module}")
        pprobe = PProbeSetup(module, module_fullname)

        sys.meta_path.insert(0, finder)

        return pprobe.module


sys.meta_path.insert(0, MetaPathFinder())
