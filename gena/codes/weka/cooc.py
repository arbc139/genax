import sys
import pymysql
import scipy
import scipy.stats
import numpy as np
import math
from multiprocessing import Manager, Pool, Process,Value
def workerPreset(j_id,mysqlId):
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3306) 
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
def worker((i,totalEdgeHit,min_sup)):
	relationIter = dict(relation)
	print("inside",i)
	for sourceEdge in dict(relationIter.items()[i*100:(i+1)*100]):
		supp = float(relation[sourceEdge]) / float(totalEdgeHit)
		support[sourceEdge] = supp
		if supp < float(min_sup):
			continue
		a = 1
		b = 1
		c = 1
		d = 1
		for targetEdge in relationIter:
			if sourceEdge[0] == targetEdge[0] or sourceEdge[0] == targetEdge[1]:
				if sourceEdge[1] == targetEdge[0] or sourceEdge[1] == targetEdge[1]:
					#1,1
					a = a + float(relation[targetEdge])
					pass
				else:
					#2,1
					b = b + float(relation[targetEdge])
					pass
			else:
				if sourceEdge[1] == targetEdge[0] or sourceEdge[1] == targetEdge[1]:
					#1,2
					c = c + float(relation[targetEdge])
					pass
				else:
					#2,2
					d = d + float(relation[targetEdge])
					pass
		lift[sourceEdge] = (a*(a+b+c+d))/ ((a+c)*(a+b))
		oddRatio[sourceEdge], pVal[sourceEdge] = scipy.stats.fisher_exact([[a,b],[c,d]])
		#LogPVal[sourceEdge] = abs(math.log((pVal[sourceEdge]+1),10))
		reversePVal[sourceEdge] = 1/(pVal[sourceEdge]+1)
		risk[sourceEdge] = (a/(a+b)) / (c/(c+d))
		obs = np.array([[a,b],[c,d]])
		chi2[sourceEdge], pChi[sourceEdge], dof, ex = scipy.stats.chi2_contingency(obs, correction=False)

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
	max_node = Value('d')
	min_node = Value('d')

	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3306) 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query = "SELECT MIN_SUP, MAX_PVAL,J_KEY FROM JOB WHERE J_ID = (%s)"
	curs.execute(query,j_id)
	row = curs.fetchone()
	min_sup = row['MIN_SUP']
	max_pval = row['MAX_PVAL']
	j_key = row['J_KEY']
	presetRunner = Process(target=workerPreset, args=(j_id,mysqlId,))
	presetRunner.start()
	presetRunner.join()

	print(relation)
	filename = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_edgeCooc.csv"
	filename_2 = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_SingleOccurringNode.csv"
	cooc = open(filename,'w')
	node_out = open(filename_2,'w')
	cooc_counter = 0
	node_counter = 0
	cooc.write("HgncId,HgncId,Weight\n")
	"""
		|	v1 	|	~v1
	---------------------
	v2	|	a	|	c
	---------------------
	~v2	|	b	|	d
	---------------------
	"""
	totalEdgeHit = 0
	relationIter = dict(relation)
	nodeIter = dict(node)

	for edge in relationIter:
		totalEdgeHit = totalEdgeHit + relation[edge]
	
	argv_list = []
	print(len(relationIter))

	for i in range(0,int(int(len(relationIter))/100)+1):
		argv_list.append((i,totalEdgeHit,min_sup))
	p = Pool(8)
	p.map(worker,argv_list)

	
	for elm in relationIter:
		if support[elm] >= min_sup:
			if pVal[elm] > max_pval:
				continue
			cooc_counter = cooc_counter+1
			cooc.write(elm[0]+","+elm[1]+","+str(reversePVal[elm])+"\n")
	node_out.write("HgncId,Weight\n")
	for nod in nodeIter:
		#print(nod, node[nod])
		#print((float(node[nod])-min_node)/(max_node-min_node))
		if min_node.value == max_node.value:
			score = str(max_node.value/len(node))
		else:
			score = str((float(node[nod])-min_node.value)/(max_node.value-min_node.value))
		node_counter = node_counter + 1
		node_out.write(nod+","+score+"\n")

	query = "UPDATE JOB SET EDGE_NUM_COOC = (%s) WHERE J_ID = (%s) ;"
	curs.execute(query ,(cooc_counter,j_id	))
	query = "UPDATE JOB SET SINGLE_OCCUR_NODE = (%s) WHERE J_ID = (%s) ;"
	curs.execute(query ,(node_counter,j_id	))
	conn.close()	


