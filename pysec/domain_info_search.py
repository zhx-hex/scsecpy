# coding:utf-8
# 免费API对域名相关信息查询 - https://api.oioweb.cn/ & http://api.btstu.cn/
# date:2023-10-17

import requests
import sys

class Domain_Info_Search:
    def __init__(self,target_domain) -> None:
        self.target_domain = target_domain
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        }

    def whois_search(self):
        tatget_url = 'https://api.oioweb.cn/api/site/whois?domain={}'.format(str(self.target_domain))
        print('\n---> ' + tatget_url)
        try:
            result = requests.get(tatget_url).json()
            if result is not None and result['code'] == 200:
                print('[域名]：' + result['result']['DomainName'])
                print('[注册商]: ' + result['result']['Registrant'])    
                print('[域名持有人/机构名称]: ' + result['result']['Holder'])
                print('[创建时间]: ' + result['result']['RegistrationTime'])
                print('[过期时间]: ' + result['result']['ExpirationTime'])
                print('[域名服务器]: ' + result['result']['DomainServer'])
                print('[域名状态]: ' + result['result']['DomainStatus'])
                print('[DNS服务器]: ' + str(result['result']['DnsServer'][0:-1]))
                return True
            else:
                print('[msg]: ' + result['msg'])
                return False

        except Exception :
            pass       

    def ICP_search(self):
        tatget_url = 'http://api.btstu.cn/icp/api.php?domain={}'.format(str(self.target_domain))
        print('\n---> ' + tatget_url)
        try:
            result = requests.get(tatget_url).json()
            if result['code'] == 200:
                print('[主办单位名称]：' + result['主办单位名称'])
                print('[主办单位性质]: ' + result['主办单位性质'])    
                print('[域名持有人/机构名称]: ' + result['域名持有人/机构名称'])
                print('[网站备案/许可证号]: ' + result['网站备案/许可证号'])
                print('[网站名称]: ' + result['网站名称'])
                print('[网站首页网址]: ' + result['网站首页网址'])
                print('[审核时间]: ' + result['审核时间'])
            else:
                print('[msg]: ' + result['msg'])

        except Exception :
            pass       


if __name__ == '__main__':

    domain_info = Domain_Info_Search(str(sys.argv[1]))
    domain_info.whois_search()
    domain_info.ICP_search()
