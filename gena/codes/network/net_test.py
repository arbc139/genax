import networkx as nx
import graph_tool.all as gt
import sys
import csv
import nx2gt_module
import pymysql
import math

j_id = sys.argv[1]
mysqlId = sys.argv[2]
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
query = "SELECT PMID_COUNT,NODE_SIZE,EDGE_NUM_ASSO,EDGE_NUM_COOC,J_KEY,COOC_EM FROM JOB where J_ID = "+j_id
curs.execute(query)
row = curs.fetchone()
node_size = row['NODE_SIZE']
edge_num_asso = row['EDGE_NUM_ASSO']
edge_num_cooc = row['EDGE_NUM_COOC']
cooc_em = int(row['COOC_EM']) + 3
pmid_count = row['PMID_COUNT']
if int(pmid_count) == 0:
    query = "UPDATE JOB SET NETWORK = 4 WHERE J_ID = (%s)"
    curs.execute(query,j_id)
    exit()
j_key = row['J_KEY']
asso_dir = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_edgeAsso.csv"
cooc_dir = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_edgeCooc.csv"
node_dir = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_SingleOccurringNode.csv"

edgeAsso = csv.reader(open(asso_dir),delimiter=';')
edgeCooc = csv.reader(open(cooc_dir),delimiter=';')
node = csv.reader(open(node_dir),delimiter=';')

edgeAssoList = []
edgeCoocList = []
nodeList = []
AssoQueryInput = []
AssoNodeQueryInput = []
CoocQueryInput = []
CoocNodeQueryInput = []
query = "UPDATE JOB_LOG SET STATUS = 0 WHERE J_ID = (%s)"
curs.execute(query,j_id)
try:
    next(node)
    for row in node:
        attributes=row[0].split(',')
        weight_dict = {}
        weight_dict['weight'] = float(attributes[1])*float(node_size)
        nodeList.append((attributes[0],weight_dict))
except:
    pass
"""try:
    next(edgeAsso)
    for row in edgeAsso:
        attributes=row[0].split(',')
        weight_dict = {}
        weight_dict['weight'] = float(attributes[cooc_em])
        edgeAssoList.append((attributes[0],attributes[1],weight_dict))
    gAsso =nx.Graph()
    gAsso.add_edges_from(edgeAssoList)

    gAssoNode = nx.Graph()
    gAssoNode = gAsso
    gtgAsso = nx2gt_module.nx2gt(gAsso)

    AssoEdgeWeight = gtgAsso.edge_properties['weight']
    AssoVertexId = gtgAsso.vertex_properties['id']
    AssoVertexIter = gtgAsso.vertices()

    AssoBetween, ep = gt.betweenness(gtgAsso,weight=AssoEdgeWeight,norm=True)
    ee, AssoEigen = gt.eigenvector(gtgAsso, weight=AssoEdgeWeight)
    #ee, AssoAuthority, AssoHub = gt.hits(gtgAsso, weight =AssoEdgeWeight)
    #AssoPagerank = gt.pagerank(gtgAsso, weight =AssoEdgeWeight)
    AssoCloseness = gt.closeness(gtgAsso,weight = AssoEdgeWeight)
    #AssoKatz = gt.katz(gtgAsso, weight = AssoEdgeWeight, beta = AssoVertexWeight)
    AssoClustering = gt.local_clustering(gtgAsso)
    AssoDegree = gtgAsso.degree_property_map("total", weight = AssoEdgeWeight)

    tempAssoList = []
    for i in AssoVertexIter:
        temp = (str(j_id), AssoVertexId[i], AssoDegree[i],
            AssoBetween[i],AssoCloseness[i],AssoEigen[i],
            AssoEigen[i],AssoClustering[i],"1")
        tempAssoNode = (str(j_id), AssoVertexId[i], AssoDegree[i],
            AssoBetween[i],AssoCloseness[i],AssoEigen[i],
            AssoEigen[i],AssoClustering[i],"2")
        temp = [None if (math.isnan(float(x)) or math.isinf(float(x))) else x for x in temp]
        tempAssoNode = [None if (math.isnan(float(x)) or math.isinf(float(x))) else x for x in tempAssoNode]
        tempAssoList.append(
            tempAssoNode
        )
        AssoQueryInput.append(
            temp
            )

    if len(nodeList) ==  0:
        AssoNodeQueryInput = tempAssoList
    else:
        gAssoNode.add_nodes_from(nodeList)
        print(gAssoNode.nodes())
        gtgAssoNode = nx2gt_module.nx2gt(gAssoNode)

        AssoNodeEdgeWeight = gtgAssoNode.edge_properties['weight']
        AssoNodeVertexId = gtgAssoNode.vertex_properties['id']
        AssoNodeVertexIter = gtgAssoNode.vertices()
        AssoNodeVertexWeight = gtgAssoNode.vertex_properties['weight']

        AssoNodeBetween,ep = gt.betweenness(gtgAssoNode,weight=AssoNodeEdgeWeight,norm=True)
        ee, AssoNodeEigen = gt.eigenvector(gtgAssoNode, weight=AssoNodeEdgeWeight)
        #ee, AssoNodeAuthority, AssoNodeHub = gt.hits(gtgAssoNode, weight =AssoNodeEdgeWeight)
        #AssoNodePagerank = gt.pagerank(gtgAssoNode, weight =AssoNodeEdgeWeight)
        AssoNodeCloseness = gt.closeness(gtgAssoNode,weight = AssoNodeEdgeWeight)
        AssoNodeKatz = gt.katz(gtgAssoNode, weight = AssoNodeEdgeWeight,beta=AssoNodeVertexWeight)
        AssoNodeClustering = gt.local_clustering(gtgAssoNode)
        AssoNodeDegree = gtgAssoNode.degree_property_map("total", weight = AssoNodeEdgeWeight)
        for i in AssoNodeVertexIter:
            temp = (str(j_id), AssoNodeVertexId[i], AssoNodeDegree[i],
                    AssoNodeBetween[i],AssoNodeCloseness[i],AssoNodeEigen[i],
                    AssoNodeKatz[i] ,AssoNodeClustering[i],"2")
            temp = [None if (math.isnan(float(x)) or math.isinf(float(x))) else x for x in temp]
            AssoNodeQueryInput.append(
                    temp
                    )


except:
    try:
        if len(nodeList) ==  0:
            AssoNodeQueryInput = tempAssoList
        if len(edgeAssoList) == 0:
            for node in nodeList:
                temp = (str(j_id),str(node[0]), "0",
                            "0","0","0",
                            str(node[1]['weight']),"0","2"
                )   
                AssoNodeQueryInput.append(
                            temp
                            )

    except:
        pass"""
try:
    next(edgeCooc)
    for row in edgeCooc:
        attributes=row[0].split(',')
        weight_dict = {}
        weight_dict['weight'] = float(attributes[cooc_em])
        edgeCoocList.append((attributes[0],attributes[1],weight_dict))
    gCooc=nx.Graph()
    gCooc.add_edges_from(edgeCoocList)

    gCoocNode= nx.Graph()
    gCoocNode = gCooc

    gtgCooc = nx2gt_module.nx2gt(gCooc)

    CoocEdgeWeight = gtgCooc.edge_properties['weight']
    CoocVertexId = gtgCooc.vertex_properties['id']
    CoocVertexIter = gtgCooc.vertices()

    CoocBetween, ep = gt.betweenness(gtgCooc,weight=CoocEdgeWeight,norm=True)
    ee, CoocEigen = gt.eigenvector(gtgCooc, weight=CoocEdgeWeight)
    #ee, CoocAuthority, CoocHub = gt.hits(gtgCooc, weight =CoocEdgeWeight)
    #CoocPagerank = gt.pagerank(gtgCooc, weight =CoocEdgeWeight)
    CoocCloseness = gt.closeness(gtgCooc,weight = CoocEdgeWeight)
    #CoocKatz = gt.katz(gtgCooc, weight = CoocEdgeWeight,beta = CoocVertexWeight)
    CoocClustering = gt.local_clustering(gtgCooc)
    CoocDegree = gtgCooc.degree_property_map("total", weight = CoocEdgeWeight)

    for i in gtgCooc.edges():
        print(CoocEdgeWeight[i])


    tempCoocList = []
    for i in CoocVertexIter:
        temp = (str(j_id), CoocVertexId[i], CoocDegree[i],
            CoocBetween[i],CoocCloseness[i],CoocEigen[i],
            CoocEigen[i],CoocClustering[i],"3")
        tempCoocNode = (str(j_id), CoocVertexId[i], CoocDegree[i],
            CoocBetween[i],CoocCloseness[i],CoocEigen[i],
            CoocEigen[i],CoocClustering[i],"4")
        temp = [None if (math.isnan(float(x)) or math.isinf(float(x))) else x for x in temp]
        tempCoocNode = [None if (math.isnan(float(x)) or math.isinf(float(x))) else x for x in tempCoocNode]
        tempCoocList.append(
            tempCoocNode
        )
        CoocQueryInput.append(
            temp
            )
    print len(nodeList)
    if len(nodeList) ==  0:
        CoocNodeQueryInput = tempCoocList
    else:
        gCoocNode.add_nodes_from(nodeList)
        gtgCoocNode = nx2gt_module.nx2gt(gCoocNode)

        CoocNodeEdgeWeight = gtgCoocNode.edge_properties['weight']
        CoocNodeVertexId = gtgCoocNode.vertex_properties['id']
        CoocNodeVertexIter = gtgCoocNode.vertices()
        CoocNodeVertexWeight = gtgCoocNode.vertex_properties['weight']

        CoocNodeBetween, ep = gt.betweenness(gtgCoocNode,weight=CoocNodeEdgeWeight,norm=True)
        ee, CoocNodeEigen = gt.eigenvector(gtgCoocNode, weight=CoocNodeEdgeWeight)
        #ee, CoocNodeAuthority, CoocNodeHub = gt.hits(gtgCoocNode, weight =CoocNodeEdgeWeight)
        #CoocNodePagerank = gt.pagerank(gtgCoocNode, weight =CoocNodeEdgeWeight)
        CoocNodeCloseness = gt.closeness(gtgCoocNode,weight = CoocNodeEdgeWeight)
        CoocNodeKatz = gt.katz(gtgCoocNode, weight = CoocNodeEdgeWeight,beta=CoocNodeVertexWeight)
        CoocNodeClustering = gt.local_clustering(gtgCoocNode)
        CoocNodeDegree = gtgCoocNode.degree_property_map("total", weight = CoocNodeEdgeWeight)

        for i in CoocNodeVertexIter:
            temp = (str(j_id), CoocNodeVertexId[i], CoocNodeDegree[i],
                    CoocNodeBetween[i],CoocNodeCloseness[i],CoocNodeEigen[i],
                    CoocNodeKatz[i],CoocNodeClustering[i],"4")
            print(CoocNodeVertexId[i],CoocNodeVertexWeight[i])
            temp = [None if (math.isnan(float(x)) or math.isinf(float(x))) else x for x in temp]
            CoocNodeQueryInput.append(
                    temp
                    )


except:
    try:
        if len(nodeList) ==  0:
            CoocNodeQueryInput = tempCoocList
        if len(edgeCoocList) == 0:        
            for node in nodeList:
                temp = (str(j_id),str(node[0]), "0",
                            "0","0","0",
                            str(node[1]['weight']),"0","4"
                )   
                CoocNodeQueryInput.append(
                            temp
                            )

    except:
        pass


conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
query = "INSERT INTO JOB_GENE_3 (J_ID, HGNC_ID, Degree, Betweenness, Closeness, Eigenvector,Katz, ClusteringCoef, NET_ID) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))"
#curs.executemany(query,AssoQueryInput)
#curs.executemany(query,AssoNodeQueryInput)
curs.executemany(query,CoocQueryInput)
curs.executemany(query,CoocNodeQueryInput)

query = "UPDATE JOB SET NETWORK = 4 WHERE J_ID = (%s)"
curs.execute(query,j_id)
