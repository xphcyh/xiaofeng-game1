#!/usr/bin/env python
import sys

from datetime import datetime

if __name__ == '__main__':
    print("hello world")
    # 输出今天几号，几点
    print("今天是:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 输出运行结束日志
    print("运行结束")
    # 打印python版本
    print(sys.version)