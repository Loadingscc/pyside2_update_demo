#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：pyside_update 
@File ：zip_command.py
@Author ：SCC
@Date ：2022/12/5 15:15 
This program is good and not any bug. If you find Bug, it must be your problem.
"""
import os
import zipfile


def zip_command2(zip_path, wait_zip_fileORdir):
    # zip_path: 压缩包路径
    # wait_zip_fileORdir: 等待压缩的文件或者了目录
    # 使用递归实现的压缩
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        f_root_length = len(os.path.dirname(wait_zip_fileORdir))  # 父目录文本长度

        def loop_zip(f_root):
            root_list = os.listdir(f_root)  # 路径列表
            if not root_list:
                # http://www.velocityreviews.com/forums/t318840-add-empty-directory-using-zipfile.html
                root = f_root[f_root_length:].replace('\\', '/').lstrip('/')  # 根目录
                zip_info = zipfile.ZipInfo(root + '/')
                zip_file.writestr(zip_info, '')
            for path in root_list:
                file_abs_path = os.path.join(f_root, path)  # 文件绝对路径
                if os.path.isdir(file_abs_path) and not os.path.islink(file_abs_path):
                    loop_zip(file_abs_path)
                else:
                    root = file_abs_path[f_root_length:].replace('\\', '/').lstrip('/')  # 跟目录
                    if os.path.islink(file_abs_path):
                        # http://www.mail-archive.com/python-list@python.org/msg34223.html
                        zip_info = zipfile.ZipInfo(root)
                        zip_info.create_system = 3
                        # long type of hex val of '0xA1ED0000L',
                        # 建立软连接
                        zip_info.external_attr = 2716663808
                        zip_file.writestr(zip_info, os.readlink(file_abs_path))
                    else:
                        zip_file.write(file_abs_path, root, zipfile.ZIP_DEFLATED)

        loop_zip(wait_zip_fileORdir)
    return True


def unzip_command2(zip_path, unzip_path, allow_unzip_forward=[]):
    """
    :param zip_path:  压缩包路径
    :param unzip_path:  解压目录
    :param allow_unzip_forward:  允许解压路径前缀
    """
    # 保持权限和软连接解压
    # 允许解压路径前缀 例如 ["my_app.app/Contents/"] 不填则全部解压

    file = zipfile.ZipFile(zip_path)
    for info in file.infolist():
        # 检查 目标文件路径 是否在 允许解压路径前缀 中
        if len(allow_unzip_forward) > 0:
            allow_unzip = False  # 允许解压
            for path in allow_unzip_forward:
                if info.filename.startswith(path):
                    allow_unzip = True
            if not allow_unzip:
                # print("不允许解压", info.filename)
                continue

        fileName = info.filename  # 文件名
        try:
            info.filename = fileName.encode('cp437').decode('utf-8')
        except:
            pass

        target_file_path = os.path.join(unzip_path, info.filename)  # 目标文件路径
        # 解压
        power = info.external_attr >> 16  # 权限
        if os.stat.S_ISLNK(power):  # 权限 == 'lrwxr-xr-x' 权限 = stat.filemode(权限)
            link_path = file.open(info).read()  # 读入软连接的位置
            # 检查 目标文件路径 是否存在，如果存在就删除 防止创建失败
            if os.path.exists(target_file_path):
                os.remove(target_file_path)
            # ic(目标文件路径, 软连接位置)
            os.symlink(link_path, target_file_path)
        else:
            # 删除文件 重新解压
            # print("解压", 文件名)
            if os.path.exists(target_file_path):
                # 检查是否为文件
                if os.path.isfile(target_file_path):
                    os.remove(target_file_path)

            file.extract(info, path=unzip_path)
            # print("权限", stat.filemode(权限))
            # 文件是否存在
            if os.path.exists(target_file_path):
                os.chmod(target_file_path, power)

    return True