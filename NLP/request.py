import requests
import json

proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
#设置代理
url='http://shuyantech.com/api/cndbpedia/avpair?q=下推自动机'
url='https://api.ownthink.com/kg/knowledge?entity=天体测量学'
# url='https://nlp.tencentcloudapi.com/?Action=WordEmbedding&Version=2019-04-08&Text="自然语言处理"'


yang=requests.get(url,proxies=proxies)#这里返回的json数据
result=open('a.json','w')

result.write(yang.text)#yang.text将yang这个json数据以字符形式使用
result.close()#这里一定要关闭文件，不然写不进去
