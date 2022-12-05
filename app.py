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

if platform.system().lower() == 'windows':
    print('Windows系统')
elif platform.system().lower() == 'darwin':
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
elif platform.system().lower() == 'linux':
    print('Linux系统')
else:
    print('Not Found Right System')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyMainWindow = main_page()
    MyMainWindow.show()
    sys.exit(app.exec_())

