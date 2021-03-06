import networkx as nx
import sys
import csv
import pymysql
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
j_id = sys.argv[1]
mysqlId = sys.argv[2]


conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
query = "SELECT NODE_SIZE,EDGE_NUM_ASSO,EDGE_NUM_COOC FROM JOB where J_ID = "+j_id
curs.execute(query)
row = curs.fetchone()
node_size = row['NODE_SIZE']
edge_num_asso = row['EDGE_NUM_ASSO']
edge_num_cooc = row['EDGE_NUM_COOC']

asso_dir = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/net_asso.txt"
cooc_dir = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/net_cooc.txt"
node_dir = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/node.csv"
csv_F = csv.reader(open(node_dir),delimiter=';')
csv_F_2 = csv.reader(open(node_dir),delimiter=';')

asso=open(asso_dir, 'rb')
G=nx.read_edgelist(asso)
asso.close()

cooc=open(cooc_dir, 'rb')
G_2=nx.read_edgelist(cooc)
cooc.close()

asso_dict ={}
asso_node_dict={}
cooc_dict={}
cooc_node_dict = {}
node_dict ={}

if len(G) != 0:

	degree = nx.degree_centrality(G)
	for node in degree:
		asso_dict[node] = [str(degree[node])]

	betweenness = nx.betweenness_centrality(G)
	for node in betweenness:
		asso_dict[node].append(str(betweenness[node]))

	closeness = nx.closeness_centrality(G)
	for node in closeness:
		asso_dict[node].append(str(closeness[node]))

	load = nx.load_centrality(G)
	for node in load:
		asso_dict[node].append(str(load[node]))

	harmonic = nx.harmonic_centrality(G)
	for node in harmonic:
		asso_dict[node].append(str(harmonic[node]))

	"""if(edge_num_asso == 1):
		eigenvector = nx.eigenvector_centrality(G)
		for node in eigenvector:
			asso_dict[node].append(str(eigenvector[node]))

		ktaz = nx.katz_centrality(G)
		for node in ktaz:
			asso_dict[node].append(str(ktaz[node]))
	
	else:
		try:
			eigenvector = nx.eigenvector_centrality_numpy(G)
			for node in eigenvector:
				asso_dict[node].append(str(eigenvector[node]))
			ktaz = nx.katz_centrality_numpy(G)
			for node in ktaz:
				asso_dict[node].append(str(ktaz[node]))
		except:
			eigenvector = nx.eigenvector_centrality(G)
			for node in eigenvector:
				asso_dict[node].append(str(eigenvector[node]))

			ktaz = nx.katz_centrality(G)
			for node in ktaz:
				asso_dict[node].append(str(ktaz[node]))"""
	


	
	for row in csv_F:
		#print (row[0])
		attributes=row[0].split(',')
		node_dict[attributes[0]]=attributes[1]
		G.add_node(attributes[0], weight = float(attributes[1])*float(node_size))

	degree = nx.degree_centrality(G)
	for node in degree:
		asso_node_dict[node] = [str(degree[node])]

	betweenness = nx.betweenness_centrality(G)
	for node in betweenness:
		asso_node_dict[node].append(str(betweenness[node]))

	closeness = nx.closeness_centrality(G)
	for node in closeness:
		asso_node_dict[node].append(str(closeness[node]))

	load = nx.load_centrality(G)
	for node in load:
		asso_node_dict[node].append(str(load[node]))

	harmonic = nx.harmonic_centrality(G)
	for node in harmonic:
		asso_node_dict[node].append(str(harmonic[node]))

	"""if(edge_num_asso == 1):
		eigenvector = nx.eigenvector_centrality(G)
		for node in eigenvector:
			asso_node_dict[node].append(str(eigenvector[node]))

		ktaz = nx.katz_centrality(G)
		for node in ktaz:
			asso_node_dict[node].append(str(ktaz[node]))
	
	else:
		try:
			eigenvector = nx.eigenvector_centrality_numpy(G)
			for node in eigenvector:
				asso_node_dict[node].append(str(eigenvector[node]))
			ktaz = nx.katz_centrality_numpy(G)
			for node in ktaz:
				asso_node_dict[node].append(str(ktaz[node]))
		except:
			eigenvector = nx.eigenvector_centrality(G)
			for node in eigenvector:
				asso_node_dict[node].append(str(eigenvector[node]))

			ktaz = nx.katz_centrality(G)
			for node in ktaz:
				asso_node_dict[node].append(str(ktaz[node]))"""
if len(G_2) != 0:
	degree = nx.degree_centrality(G_2)
	for node in degree:
		cooc_dict[node] = [str(degree[node])]

	betweenness = nx.betweenness_centrality(G_2)
	for node in betweenness:
		cooc_dict[node].append(str(betweenness[node]))

	closeness = nx.closeness_centrality(G_2)
	for node in closeness:
		cooc_dict[node].append(str(closeness[node]))

	load = nx.load_centrality(G_2)
	for node in load:
		cooc_dict[node].append(str(load[node]))

	harmonic = nx.harmonic_centrality(G_2)
	for node in harmonic:
		cooc_dict[node].append(str(harmonic[node]))

	"""if(edge_num_asso == 1):
		eigenvector = nx.eigenvector_centrality(G_2G)
		for node in eigenvector:
			cooc_dict[node].append(str(eigenvector[node]))

		ktaz = nx.katz_centrality(G_2)
		for node in ktaz:
			cooc_dict[node].append(str(ktaz[node]))
	
	else:
		try:
			eigenvector = nx.eigenvector_centrality_numpy(G_2)
			for node in eigenvector:
				cooc_dict[node].append(str(eigenvector[node]))
			ktaz = nx.katz_centrality_numpy(G_2)
			for node in ktaz:
				cooc_dict[node].append(str(ktaz[node]))
		except:
			eigenvector = nx.eigenvector_centrality(G_2)
			for node in eigenvector:
				cooc_dict[node].append(str(eigenvector[node]))

			ktaz = nx.katz_centrality(G_2)
			for node in ktaz:
				cooc_dict[node].append(str(ktaz[node]))"""
	for row in csv_F_2:
		#print (row[0])
		attributes=row[0].split(',')
		node_dict[attributes[0]]=attributes[1]
		G_2.add_node(attributes[0], weight = float(attributes[1])*float(node_size))

	degree = nx.degree_centrality(G_2)
	for node in degree:
		cooc_node_dict[node] = [str(degree[node])]

	betweenness = nx.betweenness_centrality(G_2)
	for node in betweenness:
		cooc_node_dict[node].append(str(betweenness[node]))

	closeness = nx.closeness_centrality(G_2)
	for node in closeness:
		cooc_node_dict[node].append(str(closeness[node]))

	load = nx.load_centrality(G_2)
	for node in load:
		cooc_node_dict[node].append(str(load[node]))

	harmonic = nx.harmonic_centrality(G_2)
	for node in harmonic:
		cooc_node_dict[node].append(str(harmonic[node]))

	"""if(edge_num_asso == 1):
		eigenvector = nx.eigenvector_centrality(G_2G)
		for node in eigenvector:
			cooc_node_dict[node].append(str(eigenvector[node]))

		ktaz = nx.katz_centrality(G_2)
		for node in ktaz:
			cooc_node_dict[node].append(str(ktaz[node]))
	
	else:
		try:
			eigenvector = nx.eigenvector_centrality_numpy(G_2)
			for node in eigenvector:
				cooc_node_dict[node].append(str(eigenvector[node]))
			ktaz = nx.katz_centrality_numpy(G_2)
			for node in ktaz:
				cooc_node_dict[node].append(str(ktaz[node]))
		except:
			eigenvector = nx.eigenvector_centrality(G_2)
			for node in eigenvector:
				cooc_node_dict[node].append(str(eigenvector[node]))

			ktaz = nx.katz_centrality(G_2)
			for node in ktaz:
				cooc_node_dict[node].append(str(ktaz[node]))"""
curs.close()
asso_list = []
asso_node_list = []
cooc_list = []
cooc_node_list = []
for node in asso_dict:
	asso_list.append((str(j_id), node, asso_dict[node][0],asso_dict[node][1],asso_dict[node][2],asso_dict[node][3],asso_dict[node][4],asso_dict[node][5],asso_dict[node][6],"1"))
for node in asso_node_dict:
	asso_list.append((str(j_id), node, asso_node_dict[node][0],asso_node_dict[node][1],asso_node_dict[node][2],asso_node_dict[node][3],asso_node_dict[node][4],asso_node_dict[node][5],asso_node_dict[node][6],"2"))
for node in cooc_dict:
	asso_list.append((str(j_id), node, cooc_dict[node][0],cooc_dict[node][1],cooc_dict[node][2],cooc_dict[node][3],cooc_dict[node][4],cooc_dict[node][5],cooc_dict[node][6],"3"))
for node in cooc_node_dict:
	asso_list.append((str(j_id), node, cooc_node_dict[node][0],cooc_node_dict[node][1],cooc_node_dict[node][2],cooc_node_dict[node][3],cooc_node_dict[node][4],cooc_node_dict[node][5],cooc_node_dict[node][6],"4"))
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
query = "INSERT INTO JOB_GENE_2 (J_ID, HGNC_ID, Degree, Betweenness, Closeness, Load_value, Harmonic, Eigenvector, Ktaz, NET_ID) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))"
curs.executemany(query,asso_list)

query = "UPDATE JOB SET NETWORK = 4 WHERE J_ID = (%s)"
curs.execute(query,j_id)

