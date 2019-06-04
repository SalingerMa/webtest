# -*- coding: utf-8 -*-
"""执行所有接口测试用例的主程序"""

import time, sys
sys.path.append('./interface')
sys.path.append('./db_fixture')

from htmltestrunner import HTMLTestRunner
import unittest
from db_fixture import test_data

# 指定测试用例为当前文件夹下的interface目录
test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')

if __name__ == '__main__':
    test_data.init_data()  # 初始化数据
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './repoter/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title="Guest Manage System Interface Test",
                            description="Implementation Example with:",
                            )
    runner.run(discover)
    fp.close()
