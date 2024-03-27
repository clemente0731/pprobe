import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
boot_dir = os.path.join(current_dir, 'bootstrap')


def main():
    args = sys.argv[1:]
    os.environ['PYTHONPATH'] = boot_dir
    # 执行后面的 python 程序命令
    # sys.executable 是 python 解释器程序的绝对路径 ``which python``

    print("sys.executable", sys.executable)
    print("sys.argv", sys.argv)
    os.execl(sys.executable, sys.executable, *args)

if __name__ == '__main__':
    main()