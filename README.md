当然，以下是格式化为 Markdown 的整个文档：

```markdown
# pprobe: Python Hook Tool

Welcome to the pprobe repository, a powerful Python hook tool designed to enhance your development and debugging experience. This tool provides a variety of features that can help you trace function calls, manage device conversions, and much more. Below is an overview of the project, its installation process, usage, and contribution guidelines.

## Overview

pprobe is a versatile Python package that allows you to:

- Trace and log function calls within your Python applications.
- Detect and log device conversions for tensors in PyTorch.
- Utilize a command-line interface to enable or disable specific options.

The tool is particularly useful for debugging complex Python applications, especially those involving deep learning frameworks like PyTorch.

## Installation

To install pprobe, clone the repository and use pip to install the package and its dependencies:

```sh
git clone https://github.com/your-username/pprobe.git
cd pprobe
pip install -r requirements.txt
python setup.py install
```

## Usage

pprobe can be used in various ways depending on your needs:

### Basic Usage

To start using pprobe in your Python script, you can import and initialize it as follows:

```python
from pprobe.bootstrap import TorchFunctionContext

context = TorchFunctionContext()
context.__enter__()

# Your code here

context.__exit__()
```

### Command Line Interface

pprobe comes with a command-line interface that allows you to enable, disable, list, and reset options. Here are some examples:

**List current status:**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --list
```

**Enable specific options:**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --enable option1,option2
```

**Disable specific options:**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --disable option1,option2
```

**Reset options to default:**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --reset
```

### PyTorch Specific Hooks

For PyTorch users, pprobe provides specific hooks to trace tensor operations:

```python
from pprobe.bootstrap import torch_hook_fn

torch_hook_fn('torch', torch)
```

## Contribution

Contributions to pprobe are welcome! To contribute, please follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your changes.
3. Make your changes and ensure that tests pass.
4. Submit a pull request with a detailed description of your changes.

## Testing

To run tests, use tox:

```sh
tox
```

## License

pprobe is released under the MIT License.

## Contact

For any questions or feedback, please reach out to [clemente0620@gmail.com](mailto:clemente0620@gmail.com).

Feel free to explore the code and examples provided in this repository. We hope that pprobe will be a valuable addition to your Python development toolkit. Happy coding!
```



```markdown
# pprobe: Python Hook 工具

欢迎使用 pprobe，这是一个功能强大的 Python 钩子工具，旨在提升您的开发和调试体验。该工具提供了一系列特性，可以帮助您追踪函数调用、管理 PyTorch 中的设备转换等。以下是项目的概览、安装过程、使用方法和贡献指南。

## 项目概览

pprobe 是一个多用途的 Python 包，允许您：

- 在您的 Python 应用程序中追踪和记录函数调用。
- 检测和记录 PyTorch 中张量的设备转换。
- 使用命令行界面启用或禁用特定选项。

该工具对于调试复杂的 Python 应用程序特别有用，尤其是那些涉及像 PyTorch 这样的深度学习框架。

## 安装

要安装 pprobe，请克隆仓库并使用 pip 安装包及其依赖项：

```sh
git clone https://github.com/your-username/pprobe.git
cd pprobe
pip install -r requirements.txt
python setup.py install
```

## 使用方法

pprobe 可以根据需要以多种方式使用：

### 基本使用

在您的 Python 脚本中使用 pprobe，可以按以下方式导入和初始化：

```python
from pprobe.bootstrap import TorchFunctionContext

context = TorchFunctionContext()
context.__enter__()

# 这里是您的代码

context.__exit__()
```

### 命令行界面

pprobe 配备了命令行界面，允许您启用、禁用、列出和重置选项。以下是一些示例：

**列出当前状态：**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --list
```

**启用特定选项：**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --enable option1,option2
```

**禁用特定选项：**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --disable option1,option2
```

**重置选项为默认：**

```sh
PPROBE_ENABLE=1 python -m pprobe.cli --reset
```

### PyTorch 特定钩子

对于 PyTorch 用户，pprobe 提供了特定的钩子来追踪张量操作：

```python
from pprobe.bootstrap import torch_hook_fn

torch_hook_fn('torch', torch)
```

## 贡献

欢迎对 pprobe 做出贡献！要贡献，请遵循以下步骤：

1. fork 该仓库并将其克隆到您的本地机器。
2. 为您的更改创建一个新的分支。
3. 进行您的更改并确保测试通过。
4. 提交一个拉取请求，附带您更改的详细描述。

## 测试

要运行测试，请使用 tox：

```sh
tox
```

## 许可

pprobe 在 MIT 许可证 下发布。

## 联系

如有任何问题或反馈，请通过 [clemente0620@gmail.com](mailto:clemente0620@gmail.com) 联系。

请随意浏览此仓库中提供的代码和示例。我们希望 pprobe 将成为您 Python 开发工具包中的宝贵补充。编码愉快！
```

你可以将这个内容直接复制到 GitHub 上的 `README.md` 文件中。