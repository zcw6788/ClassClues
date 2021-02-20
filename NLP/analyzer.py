import pdfreader
import textEdit
from ltp import LTP
import time

def getHEA(dep,seg):
    tempHEAword=[]
    for item in dep:
        if item[2] == "HED":
            tempHEAword.append(item[0] - 1)
    for item in dep:
        if item[2] == "COO" and (item[1] - 1 in tempHEAword) :
            tempHEAword.append(item[0] - 1)
    return tempHEAword

#判断某词是否满足关键词的基本条件
def isQualified(word):
    #表明是否为中文代词
    pronoun=["你","我","它","他","她","你们","我们","它们","他们","她们","这","那"]
    #表明标点符号的集合
    punc="~!@#$%^&*()_+-*/<>,.[]\/，。：“”\'\""
    #判断是否是名词
    # if pos[index][word]!='n':
    #     return False
    #判断是否是代词
    if word in (pronoun or punc):
        return False
    elif word.isalnum():
        return True

def standardizationKeyword(keyword):
    #过滤掉关键词中的标点
    punc = "~!@#$%^&*()_+-*/<>,.[]\/，。：“”\'\""
    for item in punc:
        if item in keyword:
            keyword=keyword.replace(item,'')
    #过滤掉关键词中的字母与数字
    for item in keyword:
        if (item >='A' and item<='z') or (item >='0' and item<='9'):
            keyword=keyword.replace(item,'')
    return keyword

#获取短语开始部分
def getBeginPosition(word,dep,seg):
    p = seg.index(word) + 1
    Position = []
    Position.append(p)
    #判断是否所有相关词语都已加入
    flag=0
    while flag!=1:
        flag=1
        for item in dep:
            if (item[1] in Position and item[0] not in Position):
                Position.append(item[0])
                flag=0
    return min(Position)


#将连续的词语拼接成句子
def getTogether(seg,beginPosition,endPosition):
    str = seg[beginPosition-1]
    # 将涉及的词语拼接成句子
    if (beginPosition < endPosition):
        if (endPosition - beginPosition > 1):
            for count in range(beginPosition, endPosition):
                str += seg[count]
        else:
            str += seg[endPosition]
    return str


#将词语扩展
def expandWord(word,dep,seg):
    beginPosition=getBeginPosition(word,dep,seg)
    str=getTogether(seg,beginPosition,seg.index(word) + 1)
    return str


# 获取一个句子中所包含的三元组关系
def getTriad(dep,seg,pos):
    #首先获取主谓之间的关系
    HEAword=getHEA(dep,seg)
    result=[]
    for HEAItem in HEAword:
        p=HEAItem+1
        #默认是不存在主语与宾语
        subjectPosition=objectPosition=-1
        #先找到句子的主语与宾语
        for item in dep:
            if(item[1]==p and item[2]=='SBV'):
                #排除主语是代词的可能
                if(isQualified(seg[item[0]-1])):
                    subjectPosition=item[0]
            elif(item[1]==p and item[2]=='VOB'):
                if (isQualified(seg[item[0] - 1])):
                    objectPosition=item[0]
        stsus='v'#表示状态是主谓宾的三元组
        for item in dep:
            if(subjectPosition!=-1 and item[1]== subjectPosition and item[2]=='ATT' and pos[item[0]-1]=='n'):
                stsus='a'#表示主语前有定语的情况
                ATTPosition=item[0]
        #将找到的词语-句子三元组输出
        if(stsus=='a' and objectPosition!=-1):
            result.append([seg[ATTPosition-1],seg[subjectPosition-1],expandWord(seg[objectPosition-1],dep,seg)])
        elif(stsus=='v' and objectPosition!=-1 and subjectPosition!=-1):
            result.append([seg[subjectPosition - 1], seg[HEAItem], expandWord(seg[objectPosition - 1],dep,seg)])
        #接着将宾语中的名词提取出来
        if(objectPosition!=-1 and subjectPosition!=-1):
            for index in range(getBeginPosition(seg[objectPosition-1],dep,seg)-1,objectPosition):
                if(pos[index-1]=='n'):
                    result.append([expandWord(seg[objectPosition-1],dep,seg),'包含',seg[index-1]])
    return result








#设置代理
proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}

start = time.time()
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
        result1=[]
for index in range(len(dep)):
    r=getTriad(dep[index],seg[index],pos[index])
    # r = getTriad(dep[8], seg[8], pos[8])
    result1.append(r)
# r=getTriad(dep[7],seg[7],pos[7])

#获取主要谓语成分
# HEAlist = getHEA(dep, seg)
#获取关键词表



end = time.time()
print (end-start)