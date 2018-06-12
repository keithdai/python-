# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import json
import sys
url='http://oooxo.com/Get_json.php'
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
data={
        'get_type':'line',
        'lineId':'0757-128-0',
        'line':1,
        'd':1,
        'City':'佛山市'
     }
response= requests.post(url,data =data,headers=headers)
print(response.text)
print(response.json())
