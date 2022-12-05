#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：pyside_update 
@File ：auto_get_version.py
@Author ：SCC
@Date ：2022/12/5 15:39 
This program is good and not any bug. If you find Bug, it must be your problem.
"""


import re
from loguru import logger
import requests

def get_new_version_and_download_path(project_name):

    url = "https://github.com/Loadingscc/pyside2_update_demo/releases/tag/V1.0.0"
    jsondata = requests.get(url)
    return re_info(jsondata.text)


def re_info(web):

    # <h1 data-view-component="true" class="d-inline mr-3">0.0.4</h1>
    # 获取版本号
    version_num = web.find('<h1 data-view-component="true" class="d-inline mr-3">')
    version_num = web[version_num + len('<h1 data-view-component="true" class="d-inline mr-3">'):]
    version_num = version_num[:version_num.find('</h1>')]
    logger.debug(version_num)

    update_info = web.find(
        '<div data-pjax="true" data-test-selector="body-content" data-view-component="true" class="markdown-body my-3">')
    update_info = web[update_info + len(
        '<div data-pjax="true" data-test-selector="body-content" data-view-component="true" class="markdown-body my-3">'):]
    update_info = update_info[:update_info.find('</div>')]
    logger.debug(update_info)

    download_address_list = []
    mac_download_addr = ""
    win_download_addr = ""
    # <a href="/Loadingscc/pyside2_update_demo/archive/refs/tags/V1.0.0.zip" rel="nofollow" data-turbo="false" data-view-component="true" class="Truncate">
    # pattern = re.compile(r'a href="(.*?)" rel="nofollow" data-skip-pjax>[\s\S].*>(.*?)</span>')
    pattern = re.compile(r'<a rel="nofollow" data-turbo="false" data-view-component="true" class="Truncate"></a>')
    result = pattern.findall(web)
    # print(result)
    logger.debug(result)
    for item in result:
        download_address = item[0]
        # https://github.com/Loadingscc/pyside2_update_demo/archive/refs/tags/V1.0.0.zip
        download_address = f"https://github.com/Loadingscc/{download_address}"
        fileName = item[1]
        download_address_list.append({fileName: download_address})

        if fileName.find('MacOS.zip') != -1:
            mac_download_addr = download_address
            mac_download_addr = "https://github.com/Loadingscc/pyside2_update_demo/archive/refs/tags/V1.0.0.tar.gz"
        if fileName.find('.exe') != -1:
            win_download_addr = download_address
            win_download_addr = "https://github.com/Loadingscc/pyside2_update_demo/archive/refs/tags/V1.0.0.zip"
    # print(下载地址列表)

    mac_download_addr = "https://github.com/Loadingscc/pyside2_update_demo/archive/refs/tags/V1.0.0.tar.gz"
    win_download_addr = "https://github.com/Loadingscc/pyside2_update_demo/archive/refs/tags/V1.0.0.zip"

    # 获取发布时间
    # <relative-time datetime="2022-07-22T17:32:41Z" class="no-wrap"></relative-time>
    realse_time = web.find('<relative-time datetime="')
    realse_time = web[realse_time + len('<relative-time datetime="'):]
    realse_time = realse_time[:realse_time.find('" class="no-wrap">')]

    return {
        "版本号": version_num,
        "下载地址列表": download_address_list,
        "更新内容": update_info,
        "发布时间": realse_time,
        "mac下载地址": mac_download_addr,
        "win下载地址": win_download_addr,
    }


if __name__ == "__main__":
    data = get_new_version_and_download_path("1")
    print(data)

