import os
import sys

enable_log_debug = bool(os.environ.get("PPROBE_LOG_DEBUG"))


class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class Logger:
    """
    implementation of Logger
    """

    @staticmethod
    def print_c(msg, color: Color):
        print(color + msg + Color.END)

    @staticmethod
    def debug(msg):
        if enable_log_debug:
            Logger.print_c("{}".format(msg), Color.RED)

    @staticmethod
    def info(msg):
        Logger.print_c("{}".format(msg), Color.GREEN)

    @staticmethod
    def warn(msg):
        Logger.print_c("WARN: {}".format(msg), Color.YELLOW)

    @staticmethod
    def error(msg):
        Logger.print_c("ERROR: {}".format(msg), Color.RED)
        sys.exit(-1)
