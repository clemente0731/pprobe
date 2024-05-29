
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


def main():
    parser = argparse.ArgumentParser(description="Enable and Disable Options")
    parser.add_argument(
        "--enable", type=str, help="Comma-separated list of options to enable"
    )
    parser.add_argument(
        "--disable", type=str, help="Comma-separated list of options to disable"
    )
    parser.add_argument("--list", action="store_true", help="List the current status")
    parser.add_argument("--reset", action="store_true", help="Reset the flags")
    args = parser.parse_args()

    print("HELLO PPROBE CLI")

    """
    ██████╗ ██████╗ ██████╗  ██████╗ ██████╗ ███████╗
    ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
    ██████╔╝██████╔╝██████╔╝██║   ██║██████╔╝█████╗  
    ██╔═══╝ ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝  
    ██║     ██║     ██║  ██║╚██████╔╝██████╔╝███████╗
    ╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝                                                                                                                                  
    """

if __name__ == "__main__":
    main()