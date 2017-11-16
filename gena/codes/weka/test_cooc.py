import sys
import pymysql
import scipy
import scipy.stats
import numpy as np
import math
from multiprocessing import Manager, Pool, Process,Value
def workerPreset(j_id,mysqlId):
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query = "SELECT D.HGNC_ID, B.PMID FROM JOB_PMID A, PMID_SUP B, SUP C, GENE D WHERE A.J_ID = "+j_id+" AND A.PMID=B.PMID AND B.S_ID = C.S_ID AND C.HGNC_ID = D.HGNC_ID AND D.HGNC_ID !='N/A' GROUP BY D.HGNC_ID, B.PMID ORDER BY PMID;"
	curs.execute(query)
	rows = curs.fetchall()
	"""relation = {}
	node = {}
	support = {}
	lift = {}
	oddRatio = {}
	pVal = {}
	risk = {}
	syms = []
	chi2 = {} 
	pChi = {}
	LogPVal = {}
	reversePVal = {}"""
	try :
		temp_pmid=rows[0]['PMID']
		#print (temp_pmid)
		#print(rows)

		for row in rows:
			if temp_pmid == row['PMID']:
				syms.append(row['HGNC_ID'])
			else:
				if len(syms) == 1:
					if syms[0] in node :
						node[syms[0]] = node[syms[0]]+1
					else :
						node[syms[0]] = 1
				else :
					syms.sort()
					for i in range(0,len(syms)):
						for j in range(i+1, len(syms)):
							if (syms[i],syms[j]) in relation:
								relation[(syms[i],syms[j])] = relation[(syms[i],syms[j])] + 1
							else :
								relation[(syms[i],syms[j])] = 1
				del syms[:]
				syms.append(row['HGNC_ID'])
				temp_pmid = row['PMID']
		if len(syms) > 1:
			syms.sort()
			for i in range(0,len(syms)):
				for j in range(i+1, len(syms)):
					if (syms[i],syms[j]) in relation:
						relation[(syms[i],syms[j])] = relation[(syms[i],syms[j])] + 1
					else :
						relation[(syms[i],syms[j])] = 1
		if len(syms) == 1:
			if syms[0] in node :
				node[syms[0]] = node[syms[0]]+1
			else :
				node[syms[0]] = 1
		#print(relation)
		#print(node)
		if len(relation) != 0:
			max_relation = float(max(relation.values()))
			min_relation = float(min(relation.values()))
		if len(node) != 0:
			max_node.value = float(max(node.values()))
			min_node.value = float(min(node.values()))
	except:
		pass
def worker((i,totalEdgeHit,min_sup,j_id,mysqlId)):
	relationIter = dict(relation)
	print("inside",i)
	"""
		|	v1 	|	~v1
	---------------------
	v2	|	a	|	c
	---------------------
	~v2	|	b	|	d
	---------------------
	"""
	for sourceEdge in dict(relationIter.items()[i*100:(i+1)*100]):
		supp = float(relation[sourceEdge]) / float(totalEdgeHit)
		support[sourceEdge] = supp
		if supp < float(min_sup):
			continue
		a = 1
		b = 1
		c = 1
		d = 1
		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		
		#a
		a = a+relation[sourceEdge]

		#b
		query = "SELECT COALESCE(SUM(HIT),0) AS HIT FROM RELATION_"+j_id+" WHERE (SOURCE = (%s) AND TARGET != (%s)) OR (SOURCE != (%s) AND TARGET = (%s))"
		curs.execute(query,(sourceEdge[0],sourceEdge[1],sourceEdge[1],sourceEdge[0]))
		row = curs.fetchone()
		try:
			b = b+float(row['HIT'])
		except:
			print(sourceEdge[0],sourceEdge[1],"b")
		#c
		query = "SELECT COALESCE(SUM(HIT),0) AS HIT FROM RELATION_"+j_id+" WHERE (SOURCE = (%s) AND TARGET != (%s)) OR (SOURCE != (%s) AND TARGET = (%s))"
		curs.execute(query,(sourceEdge[1],sourceEdge[0],sourceEdge[0],sourceEdge[1]))
		row = curs.fetchone()
		try:
			c = c+float(row['HIT'])
		except:
			print(sourceEdge[0],sourceEdge[1],"c")
		#d
		"""query = "SELECT CAST(SUM(HIT) AS SIGNED) AS HIT FROM RELATION_"+j_id+" WHERE (SOURCE != (%s) AND TARGET != (%s)) OR (SOURCE != (%s) AND TARGET != (%s))"
		curs.execute(query,(sourceEdge[0],sourceEdge[1],sourceEdge[1],sourceEdge[0]))
		row = curs.fetchone()"""
		d = d+float((float(totalEdgeHit)-a-b-c+3))

		#print(sourceEdge[0],sourceEdge[1], a,b,c,d,(a+b+c+d))
		lift[sourceEdge] = (a*(a+b+c+d))/ ((a+c)*(a+b))
		oddRatio[sourceEdge], pVal[sourceEdge] = scipy.stats.fisher_exact([[a,b],[c,d]])
		try:
			LogPVal[sourceEdge] = abs(math.log((pVal[sourceEdge]),10))
		except:
			pass
		reversePVal[sourceEdge] = 1/(pVal[sourceEdge]+1)
		#risk[sourceEdge] = (a/(a+b)) / (c/(c+d))
		obs = np.array([[a,b],[c,d]])
		chi2[sourceEdge], pChi[sourceEdge], dof, ex = scipy.stats.chi2_contingency(obs, correction=False)
		phi[sourceEdge] = math.sqrt(chi2[sourceEdge]/(a+b+c+d))
		contingency[sourceEdge] = math.sqrt(chi2[sourceEdge]/(chi2[sourceEdge]+a+b+c+d))

if __name__ == '__main__':
    j_id = sys.argv[1]
    mysqlId = sys.argv[2]
    relation = Manager().dict()
    support = Manager().dict()
    lift = Manager().dict()
    pVal = Manager().dict()
    risk = Manager().dict()
    syms = Manager().list()
    chi2 = Manager().dict()
    pChi = Manager().dict()
    LogPVal = Manager().dict()
    node = Manager().dict()
    oddRatio = Manager().dict()
    reversePVal = Manager().dict()
    phi = Manager().dict()
    contingency = Manager().dict()
    max_node = Value('d')
    min_node = Value('d')
    conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT MIN_SUP, MAX_PVAL,J_KEY,MIN_NODE_SUP FROM JOB WHERE J_ID = (%s)"
    curs.execute(query,j_id)
    row = curs.fetchone()
    min_sup = row['MIN_SUP']
    max_pval = row['MAX_PVAL']
    j_key = row['J_KEY']
    min_node_sup = row['MIN_NODE_SUP']
    presetRunner = Process(target=workerPreset, args=(j_id,mysqlId))
    presetRunner.start()
    presetRunner.join()

    #print(relation)
    filename = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_edgeCooc.csv"
    filename_2 = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_SingleOccurringNode.csv"
    cooc = open(filename,'w')
    node_out = open(filename_2,'w')
    cooc_counter = 0
    node_counter = 0
    cooc.write("HgncId,HgncId,P-Value,Support,Absolute Log P-Value,Odd Ratio,Lift,Chi-squared Statistic,Phi Coefficient,Contingency Coefficient\n")

    query = "CREATE TABLE RELATION_"+j_id+" (SOURCE INT, TARGET INT, HIT INT) ENGINE = MEMORY;"
    curs.execute(query)
    totalEdgeHit = 0
    relationIter = dict(relation)
    nodeIter = dict(node)

    for edge in relationIter:
        query = "INSERT INTO RELATION_"+j_id+"(SOURCE, TARGET, HIT) VALUES ((%s),(%s),(%s))"
        curs.execute(query,(str(edge[0]),str(edge[1]),str(relation[edge])))
        totalEdgeHit = totalEdgeHit + relation[edge]

    argv_list = []
    #print(len(relationIter))

    for i in range(0,int(int(len(relationIter))/100)+1):
        argv_list.append((i,totalEdgeHit,min_sup,j_id,mysqlId))
    p = Pool(8)
    p.map(worker,argv_list)

    LogPValIter = dict(LogPVal)
    for elm in relationIter:
        if support[elm] >= min_sup:
            if pVal[elm] > max_pval:
                continue
            cooc_counter = cooc_counter+1
            try:
				cooc.write(elm[0]+","+elm[1]+","+str(pVal[elm])+","+str(support[elm])+","+str(LogPVal[elm])+","+str(oddRatio[elm])+","+str(lift[elm])+","+str(chi2[elm])+","+str(phi[elm])+","+str(contingency[elm])+"\n")
            except:
				maximum = max(LogPValIter.iteritems(), key=operator.itemgetter(1))[0]
				cooc.write(elm[0]+","+elm[1]+","+str(pVal[elm])+","+str(support[elm])+","+str(LogPValIter[maximum])+","+str(oddRatio[elm])+","+str(lift[elm])+","+str(chi2[elm])+","+str(phi[elm])+","+str(contingency[elm])+"\n")
    node_out.write("HgncId,Support\n")
    node_count = sum(node.values())
    for nod in nodeIter:
        #print(nod, node[nod])
        #print((float(node[nod])-min_node)/(max_node-min_node))
        node_sup = float(node[nod]) / float(node_count)
        if node_sup < min_node_sup:
			print("out")
			continue 
        """if min_node.value == max_node.value:
            score = str(max_node.value/len(node))
        else:
            score = str((float(node[nod])-min_node.value)/(max_node.value-min_node.value))"""
        node_counter = node_counter + 1
        node_out.write(nod+","+str(node_sup)+"\n")


	curs.close()
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "UPDATE JOB SET EDGE_NUM_COOC = (%s) WHERE J_ID = (%s) ;"
    curs.execute(query ,(cooc_counter,j_id	))
    query = "UPDATE JOB SET SINGLE_OCCUR_NODE = (%s) WHERE J_ID = (%s) ;"
    curs.execute(query ,(node_counter,j_id	))
    
    query = "DROP TABLE RELATION_"+j_id+" ; "
    curs.execute(query)
    conn.close()	


