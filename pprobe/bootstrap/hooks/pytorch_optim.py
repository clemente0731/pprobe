from pprobe.utils.logging import Logger
from typing import Any, Callable, Optional


def lr_scheduler_step_method_wrapper(
    original_method: Callable, epoch: Optional[int] = None
):
    def wrapper(self) -> Any:
        lr = self.get_lr()
        Logger.info(f"[PPROBE] INIT LR ===> {lr}")
        return original_method(self, epoch)

    return wrapper


def optimizer_zero_grad_method_wrapper(
    original_method, set_to_none: bool = True
) -> None:
    def wrapper(self) -> Any:
        for group in self.param_groups:
            lr = group["lr"]
            Logger.info(f"[PPROBE] Iteration optimizer lr ===> {lr}")
        return original_method(self, set_to_none)

    return wrapper
