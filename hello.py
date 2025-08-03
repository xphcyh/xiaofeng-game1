#!/usr/bin/env python
import sys
import socket
import os

from datetime import datetime

if __name__ == '__main__':
    print("运行开始")
    # 打印python版本
    print(sys.version)
    print("hello", os.getlogin())
    # 输出电脑名称
    print("电脑名称:", socket.gethostname())
    # 输出今天几号，几点
    print("今天是:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 输出运行结束日志
    print("运行结束")
