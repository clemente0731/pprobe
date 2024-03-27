from setuptools import setup, find_packages
import os
import shutil


def move_configs_and_requirements():
    """将配置和依赖项移动到 benchflow 文件夹中。

    如果已存在名为 `benchflow` 的目录，则删除该目录及其内容。然后将名为 `configs` 和 `requirements` 以及 `patch`
    的子文件夹分别复制到 `benchflow` 中。

    Args:
        None

    Returns:
        None

    """
    # 删除已经存在的目标目录
    if os.path.exists("benchflow/configs"):
        shutil.rmtree("benchflow/configs")

    if os.path.exists("benchflow/requirements"):
        shutil.rmtree("benchflow/requirements")

    if os.path.exists("benchflow/patch"):
        shutil.rmtree("benchflow/patch")

    # 移动configs目录到benchflow目录下
    shutil.copytree("configs", "benchflow/configs")
    # 移动requirements目录到benchflow目录下
    shutil.copytree("requirements", "benchflow/requirements")
    # 移动patch目录到benchflow目录下
    shutil.copytree("patch", "benchflow/patch")


def clean_pycache():
    """
    清理当前目录及其子目录下所有以 .pyc、.pyo 和 __pycache__ 结尾的文件和文件夹。

    Args:
        None

    Returns:
        None

    """
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (
                name.endswith(".pyc")
                or name.endswith(".pyo")
                or name.endswith("__pycache__")
            ):
                os.remove(os.path.join(root, name))
                print(f"Removed pycache file: {os.path.join(root, name)}")
        for name in dirs:
            if name == "__pycache__":
                os.rmdir(os.path.join(root, name))
                print(f"Removed pycache directory: {os.path.join(root, name)}")


def read_requirements(file_path):
    """
    读取依赖项列表文件

    Args:
        file_path (str): 文件路径，要求该文件包含一行以换行符分隔的软件包名称

    Returns:
        list[str]: 返回一个包含所有依赖项名称的列表

    """
    with open(file_path) as f:
        print("benchflow install_requires:", f.read().splitlines())
        return f.read().splitlines()


def pre_setup():
    """
    移动配置文件和依赖项，并清理 pycache 文件

    Args:
        无参

    Returns:
        None

    Raises:
        无异常处理
    """
    clean_pycache()
    move_configs_and_requirements()


pre_setup()

setup(
    name="pthook",
    version="1.0.0",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=read_requirements("./requirements.txt"),
    entry_points={
        "console_scripts": [
            "pthook = pthook:pthook",
        ],
    },
    author="clemente0620",
    author_email="clemente0620@gmail.com",
    description="A hook tool for pytorch",
    long_description="A hook tool for pytorch, providing all the AI CHIPS to run torch",
    url="https://www.pthook.com/pthook",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)