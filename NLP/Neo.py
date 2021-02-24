from py2neo import Node, Relationship, Graph, NodeMatcher


#连接上neo4j数据库
def getConnection():
    return Graph(
        "http://localhost:7474",
        username="neo4j",
        password="ASDasd123"
    )

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
    x = matcher.match(getClass(a[0]), content=a[0]).first()
    if x is None:
        x = Node(getClass(a[0]), content=a[0])
    y = matcher.match(getClass(a[2]), content=a[2]).first()
    if y is None:
        y = Node(getClass(a[2]), content=a[2])
    r = Relationship(x, a[1], y)
    s = x | y | r
    graph.create(s)
    return

#删除数据库中所有数据
def deleteAllData(graph):
    graph.run('match (n) detach delete n')
    return

