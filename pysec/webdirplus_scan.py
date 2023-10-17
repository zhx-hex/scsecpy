# coding:utf-8
# WEBDIR+在线检测文件木马 - curl https://scanner.baidu.com/enqueue -F archive=@web.zip
# date:2023-10-15

import json
import os
import requests
import time
import sys

def file_scan(filename):
    try:
        scan_url = 'curl https://scanner.baidu.com/enqueue -F archive=@{}'.format(filename)
        result = json.loads(os.popen(scan_url).read())['url']
        time.sleep(3)
        descr = requests.get(result).json()[0]['data'][0]['descr']
        # print(type(descr))
        if str(descr) != 'None':
            print('\n 存在风险！[descr]: {}'.format(descr))
        else:
            print('\n 暂无风险！')
            
    except Exception :
        pass


if __name__ == '__main__':

    # 待检测文件路径
    file_name = str(sys.argv[1])

    file_scan(file_name)
    
