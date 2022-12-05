#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：pyside_update 
@File ：app.py
@Author ：SCC
@Date ：2022/12/5 09:46 
This program is good and not any bug. If you find Bug, it must be your problem.
"""
import os
import sys
import platform
import json

from PySide2.QtWidgets import *
from page.main_ui import main_page
import version

if platform.system().lower() == 'windows':
    print('Windows系统')
elif platform.system().lower() == 'darwin':
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
elif platform.system().lower() == 'linux':
    print('Linux系统')
else:
    print('Not Found Right System')


PROJECT_NAME = "胖橙/pyside_update"  # 项目名称
APP_NAME = "pyside_update.app"  # app名称
NOW_VERSION = version.version  # 当前版本
WEB_URL = "https://gitee.com/orange_too_fat/pyside_update"  # 官网地址


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyMainWindow = main_page()
    MyMainWindow.show()
    sys.exit(app.exec_())

