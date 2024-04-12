from setuptools import setup, find_packages
import os
import shutil


def read_requirements(file_path):
    """
    读取依赖项列表文件

    Args:
        file_path (str): 文件路径，要求该文件包含一行以换行符分隔的软件包名称

    Returns:
        list[str]: 返回一个包含所有依赖项名称的列表

    """
    with open(file_path) as f:
        print("pprobe install_requires:", f.read().splitlines())
        return f.read().splitlines()


setup(
    name="pprobe",
    version="1.0.0",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=read_requirements("./requirements.txt"),
    # entry_points={
    #     "console_scripts": [
    #         "pprobe = agent",
    #     ],
    # },
    author="clemente0620",
    author_email="clemente0620@gmail.com",
    description="A hook tool for python",
    long_description="A hook tool for python",
    url="https://www.pprobe.com/pprobe",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)