import os

def check_and_run_hook():
    """
    Check the environment variable. If PPROBE is enabled, then execute the _hook function;
    otherwise, print a warning message (only once).
    """
    # Check if PPROBE is enabled by checking the environment variable
    pprobe_enabled = int(os.environ.get("PPROBE_ENABLE", 0))

    if pprobe_enabled and pprobe_enabled == 1:
        # generic hook
        from pprobe.bootstrap import _generic_hook
    elif pprobe_enabled and pprobe_enabled == 2:
        # torch func hook
        from pprobe.bootstrap import torchfunc_hook
        context=torchfunc_hook.TorchFunctionContext()
        context.__enter__()
    else:
        # Print the warning message only once
        if not getattr(check_and_run_hook, 'warning_printed', False):
            # print("[PPROBE] Please set the environment variable PPROBE_ENABLE=1/2/3/4 to use pprobe.")
            setattr(check_and_run_hook, 'warning_printed', True)

# Call the function to check and run the hook
check_and_run_hook()