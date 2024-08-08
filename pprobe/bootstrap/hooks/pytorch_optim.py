from pprobe.utils.logging import Logger
from typing import Any, Callable, Optional


def optimizer_zero_grad_method_wrapper(
    original_method, set_to_none: bool = True
) -> None:
    def wrapper(self) -> Any:
        for group in self.param_groups:
            """
            group:
                dict_keys(['params', 'lr', 'momentum', 'dampening', 'weight_decay', 'nesterov', 'maximize', 'foreach', 'differentiable', 'fused', 'initial_lr'])
            """
            lr = group["lr"]
            Logger.info(f"[PPROBE] Iteration optimizer lr ===> {lr}")
        return original_method(self, set_to_none)

    return wrapper
