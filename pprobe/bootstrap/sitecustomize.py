import os

def check_and_run_hook():
    """
    Check the environment variable. If PPROBE is enabled, then execute the _hook function;
    otherwise, print a warning message (only once).
    """
    # Check if PPROBE is enabled by checking the environment variable
    pprobe_enabled = bool(os.environ.get("PPROBE_ENABLE"))

    if pprobe_enabled:
        # Import and run the hook only if PPROBE is enabled
        from pprobe.bootstrap import _generic_hook
    else:
        # Print the warning message only once
        if not getattr(check_and_run_hook, 'warning_printed', False):
            print("[PPROBE] Please set the environment variable PPROBE_ENABLE=1 to use pprobe.")
            setattr(check_and_run_hook, 'warning_printed', True)

# Call the function to check and run the hook
check_and_run_hook()