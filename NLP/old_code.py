#判断是否为定义句
# def isDefinition(index):
#     # for index in range(len(dep)):
#     if "是" in HEAlist[index]:
#         return True
#     elif "：" in seg[index]:
#         return True
#     else: return False

# #获取关键词
# def getKeyWord(index):
#     keywards=[]
#     for item in dep[index]:
#         if (item[2]=="SBV" or item[2]=="FOB" or item[2]=="VOB" or item[2]=="DBL") and seg[index][item[1]-1] in HEAlist[index]:
#             if isQualified(index,item[0]-1):
#                 seg[index][item[0]-1]=standardizationKeyword(seg[index][item[0]-1])
#                 if seg[index][item[0] - 1] != '':
#                     keywards.append(seg[index][item[0]-1])
#         elif  item[2]=="POB":
#             for tempitem in dep[index]:
#                 if tempitem[0]==item[1] and tempitem[2]=="adv" and seg[index][tempitem[1]-1] in HEAlist[index]:
#                     if isQualified(index, item[0] - 1):
#                         seg[index][item[0] - 1] = standardizationKeyword(seg[index][item[0] - 1])
#                         if seg[index][item[0] - 1]!='':
#                             keywards.append(seg[index][item[0] - 1])
#
#     return keywards

#得到的聚类的基本格式
# cluster=[[[0,'keyword1''keyword2'],
#           { 'keyword1':[],
#             'keyword2':[],
#             'keyword3':[]
#           }]
#          ]

# #构建层级目录表
# def makeCluster():
#     for index in range(len(dep)):
#         if len(keyWordList[index])==0:continue
#         else:
#             flag=0#标识该关键词是否出现
#             for item in cluster:
#                 for keyword in keyWordList[index]:
#                     if keyword in item[0] and flag==0:
#                         item[0][0]+=1
#                         for keyword in keyWordList[index]:
#                             if keyword not in item[0]:
#                                 item[0].append(keyword)
#                                 item[1][keyword]=[index]
#                             else:
#                                 item[1][keyword].append(index)
#                         # item[0]=list(set(item[0]))
#                         flag=1
#             if flag==0:
#                 cluster.append([[1],{}])
#                 for keyword in keyWordList[index]:
#                     cluster[-1][0].append(keyword)
#                     cluster[-1][1][keyword]=[index]
#
# #获取cluster中元素个数项目
# def getClusterCount(ele):
#     return ele[0][0]
#
# #将cluster进行排序并剪枝
# def clusterPruning():
#     cluster.sort(key=getClusterCount,reverse=True)
#     cluster_sort =cluster
#     #取前五项，受项为个数
#     if len(cluster_sort)>6:
#         temp=[]
#         for index in range(5):
#             if(len(cluster_sort[index][0])>10):
#                 temp.append(cluster_sort[index])
#         return temp
#     else:return cluster_sort
#
# #获取cluster中项的元素个数项目
# def getItemCount(ele):
#     return len(ele)
#
# #将cluster中的元素进行排序并剪枝
# def itemPruning(cluster):
#     for ele in cluster:
#         count=[]
#         for value in ele[1].values():
#             count.append(len(value))
#         count.sort(reverse=True)
#         #将长度不足的元素删去
#         if len(count)>5:
#             tempDic={}
#             for key in ele[1]:
#                 if len(ele[1][key])>=count[4]:
#                     tempDic[key]=ele[1][key]
#             ele[1]=tempDic
#             #接着重新构造cluster.ele
#             ele[0]=[0]
#             for key in ele[1]:
#                 for item in ele[1][key]:
#                     ele[0].append(item)
#             ele[0]=list(set(ele[0]))
#             ele[0][0]=len(ele[0])-1
#             ele[0]=[ele[0][0]]
#             for key in ele[1]:
#                 ele[0].append(key)
#         else:
#             cluster=sorted(ele[0],key=getItemCount,reverse=True)
#     return cluster

# keyWordList=[]
# for index in range(len(dep)):
#     keyWordList.append(getKeyWord(index))
# makeCluster()
# #对cluster中的内容进行进一步的剪枝处理
# cluster=clusterPruning()
# cluster=itemPruning(cluster)

# path=pdfreader.getPath()
# new_path=path.replace("pdf","txt")
# pdfReader.parse(path,new_path)
# sentences=textEdit.readText(new_path)
# sentences=ltp.sent_split([textEdit.readText(path)])
#进一步对字符串进行拆分
# for ele in sentences:
#     temp= textEdit.splitText(ele)
#     index=sentences.index(ele)
#     ele=temp[0]
#     if len(temp)>1:
#         for i in range(1,len(temp)-1):
#             sentences.insert(index+i,temp[i])