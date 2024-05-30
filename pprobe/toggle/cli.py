
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
class ToggleManager():
    def __init__(self):
        self.running_toggle = collections.OrderedDict()
        self.default_toggle = collections.OrderedDict()
        self.running_toggle_path = self.get_path("hook.toggle.running")
        self.default_toggle_path = self.get_path("hook.toggle.default")
        self._init_toggles()
        print(self.default_toggle)
        print("===================")
        print(self.running_toggle)

    def get_path(self, toggle_filename):
        with importlib.resources.path("pprobe.toggle", "__init__.py") as toggle_path:
            print("yyyyyyyy {}".format(Path(toggle_path.parent / toggle_filename)))
            return Path(toggle_path.parent / toggle_filename)

    def _init_toggles(self):
        self._load_toggles_from_file(self.default_toggle_path, self.default_toggle)
        self._load_toggles_from_file(self.running_toggle_path, self.running_toggle)

    def _load_toggles_from_file(self, file_path, toggle_dict):
        try:
            with file_path.open() as file:
                lines = file.readlines()
                toggle_dict.update(self._parse_toggles(lines))
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    def _parse_toggles(self, lines):
        toggles = collections.OrderedDict()

        for line in lines:
            # Skip lines without '=' or with '#' indicating comments
            if "=" not in line or "#" in line:
                continue

            # Split the line at the "=" character and strip spaces
            parts = line.strip().split("=")

            # Ensure that the line was split into exactly two parts (name and value)
            if len(parts) == 2:
                name, value = parts[0].strip(), parts[1].strip()
                # Convert "true" to True and "false" to False
                if value.lower() == "true":
                    toggles[name] = True
                elif value.lower() == "false":
                    toggles[name] = False
                else:
                    toggles[name] = value  # Keep as string if not "true" or "false"

        return toggles

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
    def update_toggle(self):
        self._save_toggles_to_file(self.running_toggle_path, self.running_toggle)
        self.show_status()

    # TODO
    def reset_toggle(self):
        self.running_toggle = collections.OrderedDict()
        self.running_toggle.update(self.default_toggle)
        self._save_toggles_to_file(self.running_toggle_path, self.running_toggle)
        self.show_status()


    def _save_toggles_to_file(self, file_path, toggle_dict):
        try:
            with file_path.open('w') as file:
                for name, value in toggle_dict.items():
                    value_str = "true" if value is True else "false" if value is False else value
                    file.write(f"{name}={value_str}\n")
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")


    # TODO
    def show_status(self):
        """
        when printing:
            True values in green
            False values in red
        """
        
        print(HELLO_PPROBE)
    
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


    toggle_instance = ToggleManager()

    if args.enable:
        enable_options = args.enable.split(",")
        for option in enable_options:
            toggle_instance.set_toggle(option, "True")

    if args.disable:
        disable_options = args.disable.split(",")
        for option in disable_options:
            toggle_instance.set_toggle(option, "False")

    if args.reset:
        toggle_instance.reset_toggle()

    if args.enable or args.disable:
        toggle_instance.update_toggle()

    if args.list:
        toggle_instance.show_status()


if __name__ == "__main__":
    main()