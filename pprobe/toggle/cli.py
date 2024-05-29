
# !/usr/bin/env python

"""
    pprobe command Line interface
"""

import argparse
import importlib
import importlib.resources
import os
import pkgutil
from pathlib import Path

from .tabulate import tabulate
import collections

HELLO_PPROBE = """
=================================================
██████╗ ██████╗ ██████╗  ██████╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
██████╔╝██████╔╝██████╔╝██║   ██║██████╔╝█████╗  
██╔═══╝ ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝  
██║     ██║     ██║  ██║╚██████╔╝██████╔╝███████╗
╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝                                                                                                                                  
=================================================
"""


# TODO
class ToggleManager:
    def __init__(self):
        self.running_toggle = collections.OrderedDict()
        self.default_toggle = collections.OrderedDict()
        self.running_toggle_path = self.get_path("hook.toggle.running")
        self.default_toggle_path = self.get_path("hook.toggle.default")

    def get_path(self, toggle_filename):
        with importlib.resources.path("pprobe.toggle", "__init__.py") as toggle_path:
            print("yyyyyyyy {}".format(Path(toggle_path.parent / toggle_filename)))
            return Path(toggle_path.parent / toggle_filename)

    def get_toggle(self, name):
        # Get the value of the flag with the specified name
        # and convert it to the corresponding boolean value 
        #  if the value is the string "true" or "false" (case-insensitive)
        value = self.running_toggle.get(name, False)
        if isinstance(value, str):
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
        return value

    def set_toggle(self, name, value):
        # Check if the given name exists in the running toggles dictionary
        if name in self.running_toggle:
            # If it exists, update the value associated with the name to the given value
            self.running_toggle[name] = value
        else:
            # If it does not exist, raise a ValueError and prompt the user to check their spelling
            raise ValueError(
                f"ERROR: toggle '{name}' does not exist in default, please check your spelling ~ "
            )

    # TODO
    def reset_toggle(self, name, value):
        pass

    
    # TODO
    def show_status(self):
        """
        when printing:
            True values in green
            False values in red
        """
        status_in_color = []

        for entry in flag_data:
            status = entry.value
            if entry.value == "True":
                # True显示为绿色
                status = f"\033[92m{entry.value}\033[0m"  # 绿色
            elif entry.value == "False":
                # False显示为红色
                status = f"\033[91m{entry.value}\033[0m"  # 红色

            default_status = entry.default_value
            if entry.default_value == "True":
                # True显示为绿色
                default_status = f"\033[92m{entry.default_value}\033[0m"  # 绿色
            elif entry.default_value == "False":
                # False显示为红色
                default_status = f"\033[91m{entry.default_value}\033[0m"  # 红色

            status_in_color.append((entry.name, status, default_status))

        table = tabulate(
            status_in_color,
            headers=["XFLAG-NAMES", "STATUS", "DEFAULT"],
            tablefmt="pretty",
        )
        print(f"{HELLO_PPROBE}\n\n{table}")

def main():
    parser = argparse.ArgumentParser(description="Enable and Disable Options")
    parser.add_argument(
        "--enable", type=str, help="Comma-separated list of options to enable"
    )
    parser.add_argument(
        "--disable", type=str, help="Comma-separated list of options to disable"
    )
    parser.add_argument("--list", action="store_true", help="List the current status")
    parser.add_argument("--reset", action="store_true", help="Reset the toggle")
    args = parser.parse_args()


    print(HELLO_PPROBE)

if __name__ == "__main__":
    main()