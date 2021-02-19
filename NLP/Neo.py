from py2neo import Node, Relationship,Graph

#连接上neo4j数据库
def getConnection():
    graph = Graph(
        "http://localhost:7474",
        username="neo4j",
        password="ASDasd123"
    )
    return graph

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
    graph.create(a)
    return

a = Node("Person", name="Alice")
b = Node("Person", name="Bob")
r = Relationship(a, "KNOWS", b)
s = a | b | r
test_graph=getConnection()

#往数据库中写入数据
# test_graph.create(s)

#从数据库中查找数据
# data = test_graph.run('MATCH (p:Person) return p').data()
# print(data)

