#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：pyside_update 
@File ：main_ui.py
@Author ：SCC
@Date ：2022/12/5 09:59 
This program is good and not any bug. If you find Bug, it must be your problem.
"""

import sys
from PySide2.QtWidgets import *

import version
from page.update_win import update_window
from ui.update_ui import Ui_Form

PROJECT_NAME = "Loadingscc/pyside2_update_demo"  # 项目名称
APP_NAME = "pyside_update.app"  # app名称
NOW_VERSION = version.version  # 当前版本
WEB_URL = "https://github.com/Loadingscc/pyside2_update_demo"  # 官网地址


class main_page(QWidget, Ui_Form):
    def __init__(self):
        super(main_page, self).__init__()
        self.setupUi(self)
        self.check_update()

    def check_update(self):
        self.update_window = update_window(project_name=PROJECT_NAME,
                                           app_name=APP_NAME,
                                           version=NOW_VERSION,
                                           web_address=WEB_URL)
        self.update_window.show()

