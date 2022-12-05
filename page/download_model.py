#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：pyside_update 
@File ：download_model.py
@Author ：SCC
@Date ：2022/12/5 15:33 
This program is good and not any bug. If you find Bug, it must be your problem.
"""
import time
import requests


def download_proccess_bar(url, save_path):
    # 终端的进度条
    try:
        from tqdm import tqdm
    except ImportError:
        print("请安装 pip install tqdm")
        return False

    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        print(f"文件大小 {total_length}")
        for chunk in tqdm(r.iter_content(chunk_size=1024), total=total_length / 1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return True


def download_file(url, save_add, return_func=None):
    # 回调函数例子
    #     def 进度(进度百分比, 已下载大小, 文件大小, 下载速率, 剩余时间):
    #         信息 = f"进度 {进度百分比}% 已下载 {已下载大小}MB 文件大小 {文件大小}MB 下载速率 {下载速率}MB 剩余时间 {剩余时间}秒"
    #         print(f"\r {信息}", end="")
    if return_func:
        start_time = time.time()
    r = requests.get(url, stream=True)
    with open(save_add, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        # 获取百分比 并调用回调函数
        for chunk in r.iter_content(chunk_size=10 * 1024):
            if chunk:
                f.write(chunk)
                f.flush()
                if return_func:
                    # 转化为百分比
                    process_point = int(f.tell() * 100 / total_length)  # 进度百分比
                    download_size = f.tell() / 1024 / 1024  # 已下载大小
                    file_size_MB = total_length / 1024 / 1024  # 文件大小MB
                    download_v = download_size / (time.time() - start_time)  # 下载速率MB
                    # 获取剩余时间取秒
                    sheng_time = (file_size_MB - download_size) / download_v  # 剩余时间
                    sheng_time = int(sheng_time)
                    # 所有数据保留两位小数
                    download_v = round(download_v, 2)
                    file_size_MB = round(file_size_MB, 2)
                    download_size = round(download_size, 2)
                    process_point = round(process_point, 2)
                    return_func(process_point, download_size, file_size_MB, download_v, sheng_time)
    return True