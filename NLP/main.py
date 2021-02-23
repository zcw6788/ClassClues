from ltp import LTP
import pdfreader
from Neo import getConnection, deleteAllData, getClass, writeToNeo4j
from analyzer import getTriad
from request import json2triad, getDBpedia

#设置代理
proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}

#初始化分词工具
ltp = LTP(proxies=proxies)


sentences= pdfreader.getTestFromPdf()['Text']
seg=[]
sdp=[]
dep=[]
pos=[]
cluster=[]

#对句子进行分词以及语义依存分析
for st in sentences:
    if(st!=''):
        seg_temp, hidden = ltp.seg([st])
        #  获得语义依存关系
        sdp.append(ltp.sdp(hidden)[0])
        #获得词性列表
        pos.append(ltp.pos(hidden)[0])
        #获得分词列表
        seg.append(seg_temp[0])
        #获得语法依存关系
        dep.append(ltp.dep(hidden)[0])
    #初始化储存三元组的list
    resultTriad=[]

for index in range(len(dep)):
    r=getTriad(dep[index],seg[index],pos[index])
    resultTriad.append(r)

#初始化数据库连接
graph=getConnection()
#先清除数据库中原有数据
deleteAllData(graph)

#将已有的三元组内容进行拓展
expa = []
for item in resultTriad:
    print(item)
    if(item!=[]):
        for itemInside in item:
            if (getClass(itemInside[0] )== "Word"):
                data = json2triad(getDBpedia(itemInside[0]))
                for itemEx in data:
                    expa.append(itemEx)
            if (getClass(itemInside[2]) == "Word"):
                data = json2triad(getDBpedia(itemInside[2]))
                for itemEx in data:
                    expa.append(itemEx)

#将原有内容写进数据库
for item in resultTriad:
    if (item != []):
        for itemInside in item:
            writeToNeo4j(graph, itemInside)
#将拓展的内容写进数据库
for item in expa:
    writeToNeo4j(graph, item)