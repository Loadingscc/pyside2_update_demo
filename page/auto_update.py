#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：pyside_update 
@File ：auto_update.py
@Author ：SCC
@Date ：2022/12/5 14:04 
This program is good and not any bug. If you find Bug, it must be your problem.
"""
import os
import shutil
import sys

from PySide2 import QtCore
from PySide2.QtCore import QThread
from page.zip_command import unzip_command2, zip_command2
from page.download_model import download_file, download_proccess_bar
from page.auto_get_version import get_new_version_and_download_path


def get_window_path():
    # 如果不处于编译状态反馈空
    try:
        make_path = sys._MEIPASS  # make_path 编译后路径
        return sys.argv[0]
    except Exception:
        return ""


def get_mac_app_path():
    # 获取 mac 的 app 地址
    # 如果不处于编译状态反馈空
    try:
        make_path = sys._MEIPASS
    except Exception:
        make_path = os.path.abspath(".")
        # 调试的
        # 编译后路径 = "/Users/Loading_create/Desktop/pythonproject/autotest/dist/my_app.app/Contents/MacOS"
    app_root = make_path[:make_path.rfind('/')]  # app 目录
    app_root = app_root[:app_root.rfind('/')]
    F_root = make_path[make_path.rfind('/') + 1:]  # 父目录
    if F_root == "MacOS":
        return app_root
    else:
        return ""


def update_mac_app(zip, app_name):
    # 更新自己MacOS应用
    # 资源压缩包 = "/Users/chensuilong/Desktop/pythonproject/autotest/dist/my_app.2.0.zip"
    # 应用名称 例如 my_app.app 这你的压缩包里面压缩的应用文件夹名称
    mac_app_path = get_mac_app_path()  # mac应用路径
    if mac_app_path != "":
        app_f_root = mac_app_path[:mac_app_path.rfind('/')]  # app目录父目录
        print(f"资源压缩包 {zip} app目录父目录{app_f_root} MacOs应用路径{mac_app_path}")
        if mac_app_path != "":
            unzip_command2(zip, app_f_root, [app_name + '/Contents/'])
            # 解压完成就压缩包
            os.remove(zip)
            mac_app_path = os.path.join(app_f_root, app_name)
            # QApplication.quit()
            app_name = app_name[:app_name.rfind('.')]
            command = f"killall {app_name} && open -n -a {mac_app_path}"
            os.system(command)
            return True, mac_app_path
    else:
        print("非MacOS编译环境")
        return False, ""


def update_windows_app(exe_path):
    # window更新方法
    # exe资源文件路径 = r"C:\Users\csuil\.virtualenvs\QtEsayDesigner\Scripts\dist\my_app1.0.exe"
    window_path = get_window_path()
    if window_path == "":
        print("非Window编译环境")
        return False, ""
    filename = os.path.basename(window_path)

    # 检查文件是否存在
    old_filename = window_path + ".old.bak"
    if os.path.exists(old_filename):
        # 删除文件
        os.remove(old_filename)

    os.rename(window_path, old_filename)
    shutil.move(exe_path, window_path)
    # 删除文件 这步放到启动时检查删除就好
    # os.remove(自身路径Window + ".old.bak") 这个运行中是无法删除的

    # 结束自身运行 然后重启自己
    os.execv(window_path, sys.argv)
    os.system(f"taskkill /f /im {filename}")
    return True, ""


def init():
    # 构建时测试运行是否正常的
    data = sys.argv  # 传入参数
    if len(data) == 2:
        data_1 = data[1]  # 参数1
        if data_1 == "test":
            print("app run success")
            sys.exit(0)

    # 如果在window系统中存在旧的文件则自动删除
    window_path = get_window_path()
    if window_path == "":
        # print("非Window编译环境")
        return False, ""
    # 检查文件是否存在
    old_file_name = window_path + ".old.bak"
    if os.path.exists(old_file_name):
        # 删除文件
        os.remove(old_file_name)


class download_thread(QThread):
    process_signal = QtCore.Signal(int, str)  # 进度 提示文本

    def __init__(self, *args, **kwargs):
        super(download_thread, self).__init__()
        self.window = kwargs.get('窗口')
        self.download_add = kwargs.get('下载地址')
        self.save_add = kwargs.get('保存地址')
        self.edit = kwargs.get('编辑框')
        self.proccess_bar = kwargs.get('进度条')
        self.app_name = kwargs.get('应用名称')
        self.return_func = kwargs.get('回调函数')

        self.process_signal.connect(self.refresh)
        # 绑定线程开始事件
        self.started.connect(self.ui_start)
        # 绑定线程结束事件
        self.finished.connect(self.ui_end)

    def run(self):
        if self.download_add is None:
            print("请传入下载地址")
            return

        def jindu(baifen, down_size, file_size, down_v, sheng_time):
            message = f"文件大小 {file_size}MB 速度 {down_v}MB 剩余时间 {sheng_time}秒"
            self.process_signal.emit(baifen, message)

        try:
            download_res = download_file(self.download_add, self.save_add, jindu)
            self.download_res = True
        except:
            self.download_res = False

    def ui_start(self):
        self.edit.setText(f'开始下载')

    def ui_end(self):
        print("下载结果", self.download_res)
        print("保存地址", self.download_add)
        self.return_func(self.download_res, self.download_add)
        self.edit.setText(f"下载完成 {self.download_add}")

    def refresh(self, jindu_num, information):
        if self.edit:
            self.edit.setText(str(information))
        if self.proccess_bar:
            self.proccess_bar.setValue(int(jindu_num))


class check_update_thread(QThread):
    def __init__(self, project_name, return_func=None):
        super(check_update_thread, self).__init__()
        # 绑定线程开始事件
        self.started.connect(self.ui_start)
        # 绑定线程结束事件
        self.finished.connect(self.ui_end)
        self.project_name = project_name
        self.return_func = return_func
        self.data = None

    def run(self):
        data = get_new_version_and_download_path(self.project_name)
        self.data = data

    def ui_start(self):
        pass
        # print("开始检查更新")

    def ui_end(self):
        # data = json.dumps(self.数据, indent=4, ensure_ascii=False)
        # print("检查更新结果", data)
        self.return_func(self.data)
