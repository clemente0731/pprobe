import traceback


def trace_function_call():
    """
    Trace the call stack and log each entry except the last two frames.

    This function raises an exception to capture the current call stack, extracts
    the stack trace, and logs the file name and line number of each entry in the
    stack trace. The last two frames (related to the trace_function_call itself)
    are excluded from the log.
    """
    try:
        raise Exception("Trace function call")
    except:
        # Get the call stack information
        stack_trace = traceback.extract_stack()
        # Print the stack trace information
        for stack_entry in stack_trace[:-2]:
            Logger.warn(
                f"\t\t Trace File: {stack_entry.filename}, Line: {stack_entry.lineno}"
            )
