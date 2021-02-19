import tkinter.filedialog
# from pdfminer.pdfparser import PDFParser, PDFDocument

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from numpy import median

import re

#精细中文分句
def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def tidySentence(content):
    content['Title']=cut_sent(content['Title'])
    content['Text'] = cut_sent(content['Text'])
    return content

# 从图形界面中获取路径
def getPath():
    path = tkinter.filedialog.askopenfilename()
    return path

#获取标题大小的边界
def getTitleBound(layout):
    lengthList = []
    for x in layout:
        if(x.height<100):
            lengthList.append(x.height)
    lengthList = list(set(lengthList))
    if(len(lengthList)):
        return median(lengthList)
    else:
        return 0


def parse(path):#读取pdf内容并转化为文本
    fp = open(path, 'rb')
    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument(praser)
    # 连接分析器 与文档对象
    # praser.set_document(doc)
    # doc.set_parser(praser)
    # 提供初始化密码,如果没有密码 就创建一个空的字符串
    # doc.initialize()

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
        # length_list = []
        content = {'Title': "", 'Text': ""}
        # 设计一个变量用于标题的对其
        titleCount = 0
        for page in PDFPage.create_pages(doc):  # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            bound=getTitleBound(layout)


            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    if (x.height > bound):
                        #标题一般没有明显的分割
                        titleCount+=1
                        content['Title']=str(titleCount)+'**'+content['Title']+results.replace(' ','')
                        content['Text'] = content['Text'] + '\n'+str(titleCount)+'\n'
                    else:
                        content['Text']=content['Text']+results.replace('\n','').replace(' ','')
        content=tidySentence(content)
        return content
                #     # 需要写出编码格式
                #     with open(new_path, 'a', encoding='utf-8') as f:
                #         results = x.get_text()
                        # print(results)
                        # length_list.append(len(results))
                        # if(x.height>bound):
                        #     f.write('**'+results+'**')
                        # else:
                        #     f.write(results)


def getTestFromPdf():
    path = getPath()
    new_path = path.replace("pdf", "txt")
    return parse(path)




