'''
工具类
Created By wuchao_bds on 2019/08/23

修改记录：
2019/08/23 new add

'''

import platform
import subprocess
import urllib.request
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

#公共类
class Utils:
    #获取真实公网IPv4
    def getRealIP():
        # 利用API获取含有用户ip的JSON数据
        url = "https://api.ipify.org/?format=json"
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        
        # 解析数据，获得IP
        jsonData = json.loads(html)
        return jsonData['ip']

    #获取真实公网IPv6
    def getRealIPv6():
        # 利用API获取含有用户ip的JSON数据
        url = "https://v6.ident.me/.json"
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        
        # 解析数据，获得IP
        jsonData = json.loads(html)
        return jsonData['address']

    #获取操作系统平台
    def getOpeningSystem():
        return platform.system()

    #判断是否联网
    def isOnline():
        userOs = Utils.getOpeningSystem()
        try:
            if userOs == "Windows":
                subprocess.check_call(["ping", "-n", "2", "www.baidu.com"], stdout=subprocess.PIPE)
            else:
                subprocess.check_call(["ping", "-c", "2", "www.baidu.com"], stdout=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            print("网络未连通！请检查网络")
            return False

    #从config.json中获取配置信息JSON串
    def getConfigJson():
        with open('config.json') as file:
            jsonStr = json.loads(file.read())
        return jsonStr

                
#阿里云AcsClient单实例类                       
class AcsClientSing:
    __client = None

    @classmethod
    def getInstance(self):
        if self.__client is None:
            acsDict = Utils.getConfigJson()
            self.__client = AcsClient(acsDict.get('AccessKeyId'), acsDict.get('AccessKeySecret'), 'cn-hangzhou')
        return self.__client

#获取阿里云Common Request请求类        
class CommonRequestSing:
    #私有类变量
    __request = None

    #该修饰符将实例方法变成类方法
    #,因为类方法无法操作私有的类变量，所以使用实例方法进行操作，再进行转换为类方法
    @classmethod
    def getInstance(self):
        if self.__request is None:
            self.__request = CommonRequest()
        return self.__request
