# coding:utf-8
# Python-requests/Python-bs4-lxml/edu_src自动化信息收集（fofa）
# date:2023-10-15

import requests
import time
from bs4 import BeautifulSoup
import base64


class Edu_Src:
    def __init__(self,pages=209):
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        self.target_url = 'https://src.sjtu.edu.cn/rank/firm/0/?page='
        self.pages = pages
        self.header = {}
    

    def get_edu_names(self):
        '''获取'教育漏洞平台-全国漏洞排行榜'每一页的高校单位的名称并存入到edunames.txt'''
        
        self.header['User-Agent'] = self.ua
        
        for i in range(1,self.pages+1):
            url = self.target_url + str(i)

            try:
                html = requests.get(url=url,headers=self.header).text
                print('\n--->pages[%s]:\n'%str(i))
                soup = BeautifulSoup(html,'lxml')
                tr_tags = soup.find_all('tr')

                for tr_tag in tr_tags:
                    a_tags = tr_tag.find_all('a')
                    for a_tag in a_tags:
                        edu_name = a_tag.text
                        # print(edu_name)
                        with open('eduname.txt','a+',encoding='utf-8') as f:
                            f.write(edu_name + '\n')
            
            except Exception :
                time.sleep(1)
                pass


    def fofa_search_urls(self,start_line=0,end_line=10):
        '''
        返回fofa搜索 title="xxxx大学" && country="CN" 的url
        如：title="上海交通大学" && country="CN" ----> https://fofa.info/result?qbase64=dGl0bGU9IuS4iua1t%2BS6pOmAmuWkp%2BWtpiIgJiYgY291bnRyeT0iQ04i
        '''
        
        with open('eduname.txt',encoding='utf-8') as file:
            name_lines = file.readlines()[start_line:end_line]

        urls = []
        for name in name_lines:
            fofa_search = 'title="{}" && country="CN"'.format(name.strip())
            qbase64 = base64.b64encode(fofa_search.encode()).decode()
            url = 'https://fofa.info/result?qbase64=%s'%qbase64.replace('+','%2B')
            urls.append(url)
        
        return urls


    def get_from_fofa(self,my_fofa_token,url_list):
        '''一种不采用 FOFA-API 的原始爬虫方法：利用token登陆后爬取网页'''

        self.header['User-Agent'] = self.ua
        self.header['Cookie'] = my_fofa_token

        for url in url_list:
            html = requests.get(url,headers=self.header).text
            soup = BeautifulSoup(html,'lxml')

            try:
                edu_info = soup.find_all('p',attrs={'class': 'hsxa-nav-font-size'})
                for edu in edu_info:
                    total_infos_num = edu.span.get_text()
                    pages = int(total_infos_num.replace(',', '')) / 10
                    pages = int(pages) + 1

                    # 爬取第一页到最后一页相关的域名及对应的高校机构名称并将域名存入到domains.txt
                    for page in range(1,pages):
                        search_url = url + '&page=' + str(page) + '&page_size=10'
                        print('\n----> target url: ' + search_url)
                        edu_domains = soup.find_all('span',attrs={'class': 'hsxa-host'})
                        edu_names = soup.find_all('div',attrs={'class': 'hsxa-meta-data-list-main-left hsxa-fl'})

                        domains = []
                        names = []
                        for edu_domain in edu_domains:
                            domains.append(edu_domain.a.get_text().strip())
                            with open('domains.txt','a+',encoding='utf-8') as file:
                                 for domain in domains:
                                    file.write(domain + '\n')
                        
                        for edu_name in edu_names:
                            names.append(edu_name.p.text.strip() ) 

                        for i in range(len(domains)):
                            print(domains[i] +' | '+ names[i])
            
            except Exception :
                time.sleep(1)
                pass 


if __name__ == '__main__':

    es = Edu_Src(pages=10)
    es.get_edu_names()

    url_list = es.fofa_search_urls()

    # 填入Cookie中的token即可
    my_fofa_token = ''

    es.get_from_fofa(my_fofa_token,url_list=url_list)
