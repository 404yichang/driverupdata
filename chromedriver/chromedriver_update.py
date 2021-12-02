import os
import re
import winreg
import zipfile
import requests

base_url = 'http://npm.taobao.org/mirrors/chromedriver/'
version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本号的正则表达式


def getChromeVersion():
    """通过注册表查询chrome版本"""
    try:
        #查找chrome浏览器注册表
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Google\\Chrome\\BLBeacon')
        #打开特定的key
        value, t = winreg.QueryValueEx(key, 'version')
        return value  # 返回版本号
    except WindowsError as e:
        # 没有安装chrome浏览器
        return "1.1.1"


def getChromeDriverVersion():
    """查询Chromedriver版本"""
    outstd2 = os.popen('chromedriver --version').read()
    try:
        version = outstd2.split(' ')[1]
        return version
    except Exception as e:
        return "0.0.0"


def getLatestChromeDriver(version):
    # 获取该chrome版本的最新driver版本号
    url = f"{base_url}{value}/"
    latest_version = requests.get(url).text
    print(f"与当前chrome匹配的最新chromedriver版本为: {value}")
    # 下载chromedriver
    print("开始下载chromedriver...")
    download_url = f"{base_url}{value}/chromedriver_win32.zip"
    file = requests.get(download_url)
    place='E:/study/python/python/python3.8.5/chromedriver.zip'
    with open("place", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
    print("下载完成.")
    # 解压
    f = zipfile.ZipFile("place", 'r')
    for file in f.namelist():
        f.extract(file)
    print("解压完成.")


def checkChromeDriverUpdate():
    chrome_version = getChromeVersion()
    print(f'当前chrome版本: {chrome_version}')
    driver_version = getChromeDriverVersion()
    print(f'当前chromedriver版本: {driver_version}')
    if chrome_version == driver_version:
        print("版本兼容，无需更新.")
        return
    print("chromedriver版本与chrome浏览器不兼容，更新中>>>")
    try:
        getLatestChromeDriver(chrome_version)
        print("chromedriver更新成功!")
    except requests.exceptions.Timeout:
        print("chromedriver下载失败，请检查网络后重试！")
    except Exception as e:
        print(f"chromedriver未知原因更新失败: {e}")


if __name__ == "__main__":
    checkChromeDriverUpdate()