'''
DDNS 主程序

使用阿里云的SDK发起请求
pip3 install aliyun-python-sdk-core

Created By wuchao_bds on 2019/08/23
修改记录:
2019/08/23 new add

'''

from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.acs_exception.exceptions import ClientException

from Utils import Utils,AcsClientSing,CommonRequestSing

import time,json
import argparse

def DDNS(use_v6):
    #获取服务器当前真实IP及类型
    try:
        if use_v6:
            ip = Utils.getRealIPv6()
            type = 'AAAA'
        else:
            ip = Utils.getRealIP()
            type = 'A'
        print("当前服务器IP:")
        print({'type': type, 'ip':ip},"\n")
    except:
        ip = ""
        print("获取服务器IP失败\n")

    #获取接口client及request
    client = AcsClientSing.getInstance()
    request = CommonRequestSing.getInstance()

    #读取配置表-获取域名信息
    first_domain = Utils.getConfigJson().get('First-level-domain')
    second_domain = Utils.getConfigJson().get('Second-level-domain')
    print('开始解析域名：',first_domain,' 二级域名：',second_domain,'\n')


    #调用DescribeDomainRecords接口，获取二级域名相关信息
    request.set_domain('alidns.aliyuncs.com')
    request.set_version('2015-01-09')
    request.set_action_name('DescribeDomainRecords')
    request.add_query_param('DomainName', first_domain)
    
    try:
        response = client.do_action_with_exception(request)
        # print("获取二级域名相关信息成功！")
        
        jsonObj = json.loads(response.decode("UTF-8"))
        records = jsonObj["DomainRecords"]["Record"]
       
        for each in records:
            if each["RR"] == second_domain and each["Type"] == type:
                recordId = each["RecordId"]
                al_type = each["Type"]
                al_ip = each["Value"]
                al_Status = each["Status"] 

        print("当前阿里云解析DDNS信息：")
        print({'recordId': recordId, 'al_type':al_type, 'al_ip':al_ip, 'al_Status':al_Status},'\n')
    except (ServerException,ClientException) as reason:
        print("获取二级域名相关信息失败！原因为")
        print(reason.get_error_msg())
        print("可参考:https://help.aliyun.com/document_detail/29774.html?spm=a2c4g.11186623.2.20.fDjexq#%E9%94%99%E8%AF%AF%E7%A0%81")
        print("或阿里云帮助文档")
        
         
    #调用UpdateDomainRecord接口，设置IP 
    try:
        if recordId == "":
            print("获取recordId失败,请检查云解析及相关配置")
        elif ip == "":
            print("获取IP失败,不更新")
        elif ip == al_ip:
            print("IP地址没变化，无需更新")
        else:
            request.set_domain('alidns.aliyuncs.com')
            request.set_version('2015-01-09')
            request.set_action_name('UpdateDomainRecord')
            request.add_query_param('RecordId', recordId)
            request.add_query_param('RR', second_domain)
            request.add_query_param('Type', type)
            request.add_query_param('Value', ip)
            request.add_query_param('Status', "ENABLE")
            request.add_query_param('TTL', 600)
            response = client.do_action_with_exception(request) 
            print("设置二级域名IP成功！")
    except (ServerException,ClientException) as reason:
        print("设置二级域名IP失败！原因为")
        print(reason.get_error_msg())
        print("可参考:https://help.aliyun.com/document_detail/29774.html?spm=a2c4g.11186623.2.20.fDjexq#%E9%94%99%E8%AF%AF%E7%A0%81")
        print("或阿里云帮助文档")
        
if __name__ == "__main__":
    #参数判断 ipv4 or ipv6
    parser = argparse.ArgumentParser(description='DDNS')
    parser.add_argument('-6', '--ipv6', nargs='*', default=False)
    args = parser.parse_args()
    isipv6 = isinstance(args.ipv6, list)
    
    while True:
      now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
      print('-----------',now,'-----------')

      #是否在线,掉线则等待3秒重试
      while not Utils.isOnline():
          print('服务器掉线，等待3秒后重试')
          time.sleep(3)
          continue

      #设置IP
      DDNS(isipv6)

      now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
      print('-----------',now,'-----------')
      time.sleep(600)
