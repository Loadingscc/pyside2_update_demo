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

from ui.update_ui import Ui_Form


class main_page(QWidget, Ui_Form):
    def __init__(self):
        super(main_page, self).__init__()
        self.setupUi(self)

