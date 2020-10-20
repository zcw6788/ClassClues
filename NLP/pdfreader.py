import sys
import importlib
import tkinter.filedialog
import tkinter as tk
importlib.reload(sys)
from collections import Counter
import re

from pdfminer.pdfparser import PDFParser,PDFDocument
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import os

'''
 解析pdf 文本，保存到txt文件中
'''
#path ="C:\\Users\\Anthony\\Desktop\\jd.pdf"

path = tkinter.filedialog.askopenfilename()
new_path=path.replace(".pdf",".txt")

#创建文件目录
def mkdir(path):
 
	folder = os.path.exists(path)
 
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径


def parse():
    fp = open(path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        #统计每行文字的个数
        length_list=[]

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    #需要写出编码格式
                    with open(new_path, 'a',encoding='utf-8') as f:
                        results = x.get_text()
                        #print(results)
                        length_list.append(len(results))
                        f.write(results + '\n')
        
        #判断页面最长行字数
        # length_count=Counter(length_list)
        # print(length_list)
        # Max_num=sorted(length_count)[2]
        # print(sorted(length_count))



        #对默认切断的文字进行合并处理
        # old_file=open(new_path,'r',encoding='utf-8')
        # w_str=""
        # for line in old_file:
        #     if len(line)>20:
        #         line.replace("\n","")
        #         w_str+=line
        #     else:
        #         w_str+=line
        # new_file=open(new_path,'w')
        # new_file.write(w_str)
        # old_file.close()
        # new_file.close()

if __name__ == '__main__':

    parse()