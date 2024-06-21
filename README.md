# pprobe: Python Hook Tool

Welcome to the pprobe repository, a powerful Python hook tool designed to enhance your development and debugging experience. This tool provides a variety of features that can help you trace function calls, manage device conversions, and much more. Below is an overview of the project, its installation process, usage, and contribution guidelines.

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
PPROBE --list
```

**Enable specific options:**

```sh
PPROBE --enable option1,option2
```

**Disable specific options:**

```sh
PPROBE --disable option1,option2
```

**Reset options to default:**

```sh
PPROBE --reset
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

## PPROBE CLI
```
PPROBE --list

=================================================
██████╗ ██████╗ ██████╗  ██████╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
██████╔╝██████╔╝██████╔╝██║   ██║██████╔╝█████╗  
██╔═══╝ ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝  
██║     ██║     ██║  ██║╚██████╔╝██████╔╝███████╗
╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝                                                                                                                                  
=================================================


+------------------+--------+---------+
| TOGGLE-NAMES     | STATUS | DEFAULT |
+------------------+--------+---------+
| CATCH_STEP       | False  |  False  |
| CATCH_LOSS       | False  |  False  |
| DUMP_OP          | False  |  False  |
| DUMP_MODULE      | False  |  False  |
| DUMP_DIST        | False  |  False  |
| DUMP_ALL         | False  |  False  |
| TEST_DUMP_OP     | False  |  False  |
| TEST_DUMP_MODULE | False  |  False  |
| TEST_DUMP_DIST   | False  |  False  |
+------------------+--------+---------+
```

## License

pprobe is released under the MIT License.

## Contact

For any questions or feedback, please reach out to [clemente0620@gmail.com](mailto:clemente0620@gmail.com).

Feel free to explore the code and examples provided in this repository. We hope that pprobe will be a valuable addition to your Python development toolkit. Happy coding!
```



