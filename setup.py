from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
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


class build_py_with_pth_file(build_py):
    """Include the .pth file for this project, in the generated wheel."""

    def run(self):
        super().run()

        self.copy_pth()
        self.copy_toggle()

    def copy_pth(self):
        destination_in_wheel = "pprobe.pth"
        location_in_source_tree = "pprobe.pth"
        outfile = os.path.join(self.build_lib, destination_in_wheel)
        self.copy_file(location_in_source_tree, outfile, preserve_mode=0)

    def copy_toggle(self):
        src_file = "pprobe/toggle/hook.toggle.default"
        dst_file = "pprobe/toggle/hook.toggle.running"
        dst_build_file = os.path.join(self.build_lib, dst_file)
        try:
            shutil.copyfile(src_file, dst_build_file)
            print(f"Copied {src_file} to {dst_build_file}")
        except FileNotFoundError:
            print(f"Source file {src_file} does not exist")


setup(
    name="pprobe",
    version="1.0.0",
    description="A hook tool for python",
    long_description="A hook tool for python",
    url="https://www.pprobe.com/pprobe",
    author="clemente0620",
    author_email="clemente0620@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "PPROBE=pprobe.toggle.cli:main",
        ]
    },
    packages=find_packages(exclude=["pprobe/tests"]),
    include_package_data=True,
    package_data={"": ["*.pth"]},  # 将所有.pth文件包含在安装中
    install_requires=read_requirements("./requirements.txt"),
    zip_safe=False,
    cmdclass={"build_py": build_py_with_pth_file},
)
