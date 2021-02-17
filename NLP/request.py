import requests#需要安装requests模块，详情百度pip安装
import json#下面会用到

proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
url='http://shuyantech.com/api/cndbpedia/avpair?q=互联网'
yang=requests.get(url,proxies=proxies)#这里返回的json数据
result=open('a.json','w')

result.write(yang.text)#yang.text将yang这个json数据以字符形式使用
result.close()#这里一定要关闭文件，不然写不进去