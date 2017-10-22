# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 22:17:47 2017

@author: Administrator
"""

import re, requests
from pprint import pformat

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9028'
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
str = pformat(dict(stations), indent=4)

f = open("stations.py","w",encoding='utf-8')
f.write(str)
f.close()

