## 基于阿里云实现动态IP解析

修改config文件，后台运行DDNS.py，当IP变更时，域名会自动解析

基于python3，依赖包：

```
#阿里云的SDK
pip3 install aliyun-python-sdk-core
```


config.json：
```
{
    "AccessKeyId": "LTAIt54qAAAAYW8O",                           #阿里云解析申请的key
    "AccessKeySecret": "P5ajC3H5sjFAAAANBc2D21lYaGYbj",          #阿里云解析申请的Secret
    "First-level-domain": "baidu.com",                           #一级域名  如baidu.com
    "Second-level-domain": "www"                                 #二级域名  如www
}
```

运行方法：
```
#ipv4:
nohup python -u DDNS.py >DDNS.log 2>&1 &

#ipv6:
nohup python -u DDNS.py -6 >DDNS.log 2>&1 &
```

查看日志：
```
tail -10f DDNS.log
```
