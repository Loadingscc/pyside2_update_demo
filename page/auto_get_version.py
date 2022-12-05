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
import requests

def get_new_version_and_download_path(project_name):

    url = "https://gitee.com/orange_too_fat/pyside_update.git"
    jsondata = requests.get(url)
    return 解析网页信息(jsondata.text)


def 解析网页信息(网页):
    # 读取文件 test.html
    # with open('test.html', "r", encoding="utf-8") as f:
    #     网页 = f.read()
    # print(网页)

    # <h1 data-view-component="true" class="d-inline mr-3">0.0.4</h1>
    # 获取版本号
    版本号 = 网页.find('<h1 data-view-component="true" class="d-inline mr-3">')
    版本号 = 网页[版本号 + len('<h1 data-view-component="true" class="d-inline mr-3">'):]
    版本号 = 版本号[:版本号.find('</h1>')]
    # print(版本号)
    # 获取更新内容
    # <div data-pjax="true" data-test-selector="body-content" data-view-component="true" class="markdown-body my-3"><h1>自动更新程序</h1>
    # <ul>
    # <li>更新了自动构建</li>
    # <li>自动获取版本</li>
    # <li>自动下载</li>
    # <li>自动替换</li>
    # </ul></div>
    # </div>
    更新内容 = 网页.find(
        '<div data-pjax="true" data-test-selector="body-content" data-view-component="true" class="markdown-body my-3">')
    更新内容 = 网页[更新内容 + len(
        '<div data-pjax="true" data-test-selector="body-content" data-view-component="true" class="markdown-body my-3">'):]
    更新内容 = 更新内容[:更新内容.find('</div>')]
    # print(更新内容)
    # 获取下载地址列表
    #             <a href="/duolabmeng6/qtAutoUpdateApp/releases/download/0.0.4/my_app_MacOS.zip" rel="nofollow" data-skip-pjax>
    #               <span class="px-1 text-bold">my_app_MacOS.zip</span>
    #
    #             </a>

    下载地址列表 = []
    mac下载地址 = ""
    win下载地址 = ""
    pattern = re.compile(r'a href="(.*?)" rel="nofollow" data-skip-pjax>[\s\S].*>(.*?)</span>')
    result = pattern.findall(网页)
    # print(result)
    for item in result:
        下载地址 = item[0]
        下载地址 = f"https://ghproxy.com/https://github.com{下载地址}"
        文件名 = item[1]
        下载地址列表.append({文件名: 下载地址})

        if 文件名.find('MacOS.zip') != -1:
            mac下载地址 = 下载地址
        if 文件名.find('.exe') != -1:
            win下载地址 = 下载地址
    # print(下载地址列表)

    # 获取发布时间
    # <relative-time datetime="2022-07-22T17:32:41Z" class="no-wrap"></relative-time>
    发布时间 = 网页.find('<relative-time datetime="')
    发布时间 = 网页[发布时间 + len('<relative-time datetime="'):]
    发布时间 = 发布时间[:发布时间.find('" class="no-wrap">')]

    return {
        "版本号": 版本号,
        "下载地址列表": 下载地址列表,
        "更新内容": 更新内容,
        "发布时间": 发布时间,
        "mac下载地址": mac下载地址,
        "win下载地址": win下载地址,
    }


if __name__ == "__main__":
    data = get_new_version_and_download_path("1")
    print(data)

