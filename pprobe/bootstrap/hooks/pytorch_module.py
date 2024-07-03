import torch
from contextlib import ContextDecorator


class TorchModuleContext(ContextDecorator):
    def __init__(self):
        self.hooks = []

    def __enter__(self):
        self._scan_and_register_hooks()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._remove_hooks()

    def _scan_and_register_hooks(self):
        """
        Scan the global namespace and register hooks for all torch.nn.Module instances.
        """
        print("====== _scan_and_register_hooks =========")
        for obj in globals().values():
            print(f"########################## {obj}")
            if isinstance(obj, torch.nn.Module):
                self._register_hooks_for_model(obj)

    def _register_hooks_for_model(self, model):
        m_tuple = self.get_named_modules(model)
        for name, m in m_tuple:
            self._register_hook(name, m)

    def get_named_modules(self, module):
        """
        Return a list of (name, module) tuples from the module.
        """
        return list(module.named_modules())

    def _register_hook(self, name, module):
        """
        Register a hook for the given module.
        """

        # Define the hook function
        def hook_fn(module, input, output):
            print(f"Hook for {name}: input = {input}, output = {output}")

        # Register the forward hook and store the hook handle
        handle = module.register_forward_hook(hook_fn)
        self.hooks.append(handle)

    def _remove_hooks(self):
        for handle in self.hooks:
            handle.remove()
        self.hooks = []
