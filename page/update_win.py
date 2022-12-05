#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：pyside_update 
@File ：update_win.py
@Author ：SCC
@Date ：2022/12/5 13:45 
This program is good and not any bug. If you find Bug, it must be your problem.
"""
import os
import platform
import webbrowser

from PySide2.QtWidgets import *
from ui.ui_winUpdate import Ui_Form
from page.auto_update import download_thread, update_windows_app, update_mac_app, check_update_thread


class update_window(QDialog):
    def __init__(self, project_name, app_name, version, web_address):
        super(update_window, self).__init__()
        self.project_name = project_name  # 项目名称
        self.app_name = app_name  # 应用名称
        self.version = version  # 版本
        self.web_address = web_address  # 官方网址

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('软件更新')
        self.resize(620, 380)

        # 绑定按钮事件
        self.ui.pushButton_azgx.clicked.connect(self.update)
        self.ui.pushButton_gfwz.clicked.connect(self.open_web)
        self.ui.pushButton_tgbb.clicked.connect(self.close)
        self.ui.pushButton_ok.clicked.connect(self.close)

        # 隐藏更新进度条和状态编辑框
        self.ui.progressBar.hide()
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setRange(0, 100)
        self.ui.label_zt.hide()
        self.ui.pushButton_ok.hide()
        self.ui.pushButton_azgx.setEnabled(False)
        self.ui.pushButton_tgbb.setEnabled(False)
        # textEdit 禁止编辑
        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit.setText("正在检查更新...")

        new_version = "查询中..."
        self.ui.label_2.setText(new_version)
        self.ui.label_bbh.setText(f'最新版本:{new_version} 当前版本: {self.version}')
        self.download_path = os.path.expanduser('~/Downloads')
        if platform.system().lower() == 'darwin':
            self.zip_path = os.path.abspath(self.download_path + f"/{self.app_name}.zip")
        if platform.system().lower() == 'windows':
            self.zip_path = os.path.abspath(self.download_path + f"/{self.app_name}.exe")

        print('查询最新版本')
        self.check_update_thread = check_update_thread(self.project_name, self.check_update_return)
        self.check_update_thread.start()

    def check_update_return(self, data):
        print("数据", data)
        new_version = data['版本号']
        self.ui.label_bbh.setText(f'最新版本:{new_version} 当前版本: {self.version}')
        self.ui.textEdit.setHtml(data['更新内容'])
        self.mac_download_add = data['mac下载地址']
        self.win_download_add = data['win下载地址']

        if new_version == self.version:
            self.ui.label_2.setText("你使用的是最新版本")
            self.ui.pushButton_azgx.hide()
            self.ui.pushButton_tgbb.hide()
            self.ui.pushButton_ok.show()
            return

        self.ui.pushButton_azgx.setEnabled(True)
        self.ui.pushButton_tgbb.setEnabled(True)
        self.ui.label_2.setText("发现新版本")

    def update(self):
        print('安装更新')
        self.ui.progressBar.show()
        self.ui.label_zt.show()
        self.ui.label_zt.setText('更新中...')
        self.ui.pushButton_azgx.setEnabled(False)
        self.ui.pushButton_tgbb.setEnabled(False)
        print('mac下载地址', self.mac_download_add)
        print('win下载地址', self.win_download_add)

        if platform.system().lower() == 'darwin':
            if self.mac_download_add == "":
                self.ui.label_zt.setText("没有找到 ManOS 系统软件下载地址")
                return
            print('安装更新 mac', self.mac_download_add, self.zip_path)
            self.download_thread = download_thread(
                下载地址=self.mac_download_add,
                保存地址=self.zip_path,
                窗口=self,
                编辑框=self.ui.label_zt,
                进度条=self.ui.progressBar,
                应用名称=self.app_name,
                回调函数=self.download_finish,
            )
            self.download_thread.start()

        if platform.system().lower() == 'windows':
            if self.win_download_add == "":
                self.ui.label_zt.setText("没有找到 windows 系统软件下载地址")
                return
            print('安装更新 win', self.win_download_add, self.zip_path)

            self.download_thread = download_thread(
                下载地址=self.win_download_add,
                保存地址=self.zip_path,
                窗口=self,
                编辑框=self.ui.label_zt,
                进度条=self.ui.progressBar,
                应用名称=self.app_name,
                回调函数=self.download_finish
            )
            self.download_thread.start()

    def download_finish(self, res, save_path):
        if not res:
            self.ui.label_zt.setText("下载更新失败")
            return
        if platform.system().lower() == 'darwin':
            update_mac_app(
                资源压缩包=save_path,
                应用名称=self.app_name
            )
        if platform.system().lower() == 'windows':
            exe_path = save_path
            update_windows_app(exe_path)

    def open_web(self):
        # 浏览器打开网址
        print('官方网址', self.web_address)
        webbrowser.open(self.web_address)
