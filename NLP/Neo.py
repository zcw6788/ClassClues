import py2neo
from py2neo import Node, Relationship, Graph, NodeMatcher


#连接上neo4j数据库
def getConnection():
    graph = Graph(
        "http://localhost:7474",
        username="neo4j",
        password="ASDasd123"
    )
    return graph

#区分词语与句子
def getClass(str):
    if(len(str)>3):
        return "Sentence"
    else:
        return "Word"

#新建一个节点
def createNode(category,name):
    return Node(category,name=name)

#新建一层关系
def createRelation(a,r,b):
    return Relationship(a, r, b)

#往已有节点中写入属性
def addAttributes(node,attrName,attrValue):
    return

#将数据写入数据库
def writeToNeo4j(graph,a):
    matcher = NodeMatcher(graph)
    a = matcher.match(getClass(a[0]), content=a[0]).first()
    if (a == None):
        a = Node(getClass(a[0]), content=a[0])
    b = matcher.match(getClass(a[1]), content=a[1]).first()
    if (b == None):
        b = Node(getClass(a[1]), content=a[1])
    r = Relationship(a, a[1], b)
    s = a | b | r
    graph.create(s)
    return

#删除数据库中所有数据
def deleteAllData(graph):
    graph.run('match (n) detach delete n')
    return

# graph=getConnection()
# deleteAllData(graph)
