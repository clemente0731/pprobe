import os


def check_and_run_hook():
    """
    Check the environment variable. If PPROBE is enabled, then execute the _hook function;
    otherwise, print a warning message (only once).
    """
    # Check if PPROBE is enabled by checking the environment variable
    pprobe_enabled = int(os.environ.get("PPROBE_ENABLE", 0))

    if pprobe_enabled:
        # generic hook
        from pprobe.bootstrap import hook_setup
    else:
        # Print the warning message only once
        if not getattr(check_and_run_hook, "warning_printed", False):
            # print("[PPROBE] Please set the environment variable PPROBE_ENABLE=1/2/3/4 to use pprobe.")
            setattr(check_and_run_hook, "warning_printed", True)


# Call the function to check and run the hook
check_and_run_hook()
