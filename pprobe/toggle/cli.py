
# !/usr/bin/env python

"""
    pprobe command Line interface
"""

import argparse
import collections
import os
import pkgutil
from pathlib import Path

import importlib
import importlib.resources
from .tabulate import tabulate
from dataclasses import dataclass

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


# @dataclass
# class ToggleStatus:
#     name: str
#     status: str
#     default_status: str


class ToggleManager():
    def __init__(self):
        self.default_toggle = collections.OrderedDict()
        self.running_toggle = collections.OrderedDict()
        self.default_toggle_path = self.get_path("hook.toggle.default")
        self.running_toggle_path = self.get_path("hook.toggle.running")
        self._init_toggles()

    def get_path(self, toggle_filename):
        with importlib.resources.path("pprobe.toggle", "__init__.py") as toggle_path:
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

    def get_toggles(self):
        return self.running_toggle

    def get_toggle(self, name):
        return self.running_toggle.get(name)

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

    def update_toggle(self):
        self._save_toggles_to_file(self.running_toggle_path, self.running_toggle)
        self.show_status()

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


    def show_status(self):
        """
        when printing:
            True values in green
            False values in red
        """
        
        print(HELLO_PPROBE)
        
        def colorize(value):
            """Return the value in green if True, in red if False."""
            if value in (True, "True"):
                return f"\033[92m{value}\033[0m"  # GREEN
            elif value in (False, "False"):
                return f"\033[91m{value}\033[0m"  # RED
            return value
        
        status_in_color = []

        for name, value in self.running_toggle.items():
            status = colorize(value)
            default_value = self.default_toggle.get(name, "False")
            default_status = colorize(default_value)
            status_in_color.append((name, status, default_status))

        table = tabulate(
            status_in_color,
            headers=["TOGGLE-NAMES", "STATUS", "DEFAULT"],
            tablefmt="pretty",
            colalign=("left", "center", "center"),
        )
        print(f"\n{table}\n")


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