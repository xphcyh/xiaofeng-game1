#开头加下python标识

#!/usr/bin/env python
from datetime import datetime
print("hello world")
# 输出今天几号，几点
print("今天是:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# 输出运行结束日志
print("运行结束")