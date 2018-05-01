import requests
import pymysql
import sys
import os
from xml.etree.ElementTree import parse
from lxml import etree
import re
import time
import datetime
from multiprocessing import Manager, Pool
efetch_out_list = Manager().list()
job_has_pmid = Manager().list()
new_pmid = Manager().list()
exist_pmid = Manager().list()
def worker((job_num,i)):
	print ("inside", i)
	retmax = 5000
	
	#old_time = os.stat("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/uilist.text").st_mtime
	#time_counter = 0
	#cur_time = os.stat("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/uilist.text").st_mtime
	efetch_url = base +"efetch.fcgi?db="+entrez_db+"&WebEnv="+web
	efetch_url += "&query_key="+key+"&retstart="+str(i*retmax)
	efetch_url += "&retmax="+str(retmax)+"&rettype=uilist&retmode=text&api_key=5b1bbe2ef2a0bebe85a9937c9d71e9085f09"
	while True:
		try:
			efetch_out = requests.get(efetch_url)
			counter = int(efetch_out.status_code) - 400
			counter_zero = 10/counter 
		except ZeroDivisionError as e:
			continue
		except:
			print("request failed, retry after 5 seconds")
			time.sleep(5)
			continue
		else:
			break
		if efetch_out.status_code == 200:
			break
		
	print (efetch_out.status_code)
	pattern = r"Unable to obtain query"
	m = re.search(pattern,efetch_out.text)
	if m is not None :
		print("request failed, retry after 5 seconds")
		time.sleep(5)
		#old_time = os.stat("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/uilist.text").st_mtime
	efetch_out_list.append(efetch_out.text)

def worker2((job_num,i,mysqlId)):
	step = 500000
	print ("length of job has pmid in the thread",len(job_has_pmid))
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	#query = "CREATE TEMPORARY TABLE temp_uilist_"+job_num+"_"+str(i)+"(pmid int(11));"
	query1 = "CREATE TABLE temp_uilist_"+job_num+"_"+str(i)+"(pmid int(11));"
	curs.execute(query1)
	print (query1	)
	query2 = "INSERT INTO temp_uilist_"+job_num+"_"+str(i)+" (pmid) VALUES (%s)"
	curs.executemany(query2, job_has_pmid[i*step:(i+1)*step-1])

	"""query3 = "SELECT a.pmid FROM PMID a JOIN temp_uilist_"+job_num+"_"+str(i)+" b ON a.pmid = b.pmid;"
	curs.execute(query3)
	rows = curs.fetchall()
	for row in rows:
		exist_pmid.append((job_num,row['pmid']))"""
	curs.close()
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query4 = "SELECT STRAIGHT_JOIN a.pmid FROM temp_uilist_"+job_num+"_"+str(i)+" a LEFT JOIN PMID b ON a.pmid = b.pmid WHERE b.pmid IS NULL;"
	curs.execute(query4)
	rows = curs.fetchall()
	for row in rows:
		new_pmid.append(str(row['pmid']))
	curs.close()
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query1 = "DROP  TABLE temp_uilist_"+job_num+"_"+str(i)
	curs.execute(query1)
def worker3((job_num,i,mysqlId)):
	step = 500000
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query = "INSERT IGNORE INTO JOB_PMID (J_ID, PMID) VALUES (%s,%s)"
	curs.executemany(query, exist_pmid[i*step:(i+1)*step-1])
if __name__ == '__main__':


	job_num = sys.argv[1]
	mysqlId = sys.argv[2]
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query = "SELECT * FROM JOB where J_ID ="+job_num
	curs.execute(query)
	row = curs.fetchone()
	print(row['QUERY'], row['START_DATE'], row['END_DATE'])
	query_string = "("+row['QUERY']+")"
	#+" AND (\""+str(row['START_DATE'])+"\"[Date - Create] : \""+str(row['END_DATE'])+"\"[Date - Create]) "
	print (query_string)
	#row_start = datetime.datetime.strptime( str(row['START_DATE']), "%Y-%m-%d").strftime("%Y/%m/%d")
	#row_end = datetime.datetime.strptime( str(row['END_DATE']), "%Y-%m-%d").strftime("%Y/%m/%d")
	row_start = row['START_DATE'].strftime('%Y/%m/%d')
	row_end = row['END_DATE'].strftime('%Y/%m/%d')
	query ="SELECT J_ID,QUERY, START_DATE, END_DATE FROM JOB WHERE J_ID != (%s) AND NETWORK = 4 AND TOO_SMALL != 1 AND QUERY=(%s) AND START_DATE >= (%s) AND END_DATE <= (%s) ORDER BY DATEDIFF(END_DATE,START_DATE) DESC;"
	curs.execute(query, (job_num,row['QUERY'],  row['START_DATE'],row['END_DATE']))
	row2 = curs.fetchone()
	query ="SELECT J_ID,QUERY, START_DATE, END_DATE FROM JOB WHERE J_ID != (%s) AND NETWORK = 4 AND QUERY=(%s)  AND END_DATE <= (%s) AND DATEDIFF((%s),START_DATE) < 365 ORDER BY START_DATE DESC;"
	curs.execute(query, (job_num,row['QUERY'],  row['END_DATE'],row['START_DATE']))
	row3 = curs.fetchone()
	delete_string = ""
	if row2 is not None:
		print(row2)
		query ="INSERT IGNORE INTO JOB_PMID (J_ID,PMID) SELECT (%s), PMID FROM JOB_PMID WHERE J_ID =(%s)"
		curs.execute(query,(job_num,row2['J_ID']))
		print(row['START_DATE'], row['END_DATE'], row2['START_DATE'], row2['END_DATE'])
		#row2_start = datetime.datetime.strptime( str(row2['START_DATE']), "%Y-%m-%d").strftime("%Y/%m/%d")
		#row2_end = datetime.datetime.strptime( str(row2['END_DATE']), "%Y-%m-%d").strftime("%Y/%m/%d")
		row2_start = row2['START_DATE'].strftime('%Y/%m/%d')
		row2_end = row2['END_DATE'].strftime('%Y/%m/%d')
		period = " AND ((\""+str(row_start)+"\"[Date - Entrez] : \""+str(row2_start)+"\"[Date - Entrez]) OR (\""+str(row2_end)+"\"[Date - Entrez] : \""+str(row_end)+"\"[Date - Entrez]))"
		query_string += period
	elif row3 is not None :
		print(row3)
		query ="INSERT IGNORE INTO JOB_PMID (J_ID,PMID) SELECT (%s), PMID FROM JOB_PMID WHERE J_ID =(%s)"
		curs.execute(query,(job_num,row3['J_ID']))
		print (row3['J_ID'])
		#row3_start = datetime.datetime.strptime( str(row3['START_DATE']), "%Y-%m-%d").strftime("%Y/%m/%d")
		#row3_end = datetime.datetime.strptime( str(row3['END_DATE']), "%Y-%m-%d").strftime("%Y/%m/%d")
		row3_start = row3['START_DATE'].strftime('%Y/%m/%d')
		row3_end = row3['END_DATE'].strftime('%Y/%m/%d')
		print(query)
		print(row['START_DATE'], row['END_DATE'], row3['START_DATE'], row3['END_DATE'])
		period = " AND ((\""+str(row3_end)+"\"[Date - Entrez] : \""+str(row_end)+"\"[Date - Entrez]))"
		delete_period = " AND ((\""+str(row3_start)+"\"[Date - Entrez] : \""+str(row['START_DATE']-datetime.timedelta(days=1))+"\"[Date - Entrez]))"
		delete_string = query_string + delete_period
		#query_string += " AND (\""+str(row3_end)+"\"[Date - Entrez] : \""+str(row_end)+"\"[Date - Entrez] OR (\""+str(row_start)+"\"[Date - Entrez] : \""+str(row_start)+"\"[Date - Entrez])OR (\""+str(row_end)+"\"[Date - Entrez] : \""+str(row_end)+"\"[Date - Entrez])) "
		query_string += " AND ((\""+str(row_start)+"\"[Date - Entrez] : \""+str(row_end)+"\"[Date - Entrez]) )"
	else:
		query_string += " AND ((\""+str(row_start)+"\"[Date - Entrez] : \""+str(row_end)+"\"[Date - Entrez]) )"
	print(query_string)
	entrez_db = 'pubmed'
	#query = row['QUERY']
	#assemble the esearch URL
	base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
	url = base + "esearch.fcgi?db="+entrez_db+"&term="+query_string+"&usehistory=y";

	#do esearch
	output = requests.get(url)

	#save esearch result
	if not os.path.exists("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/"):
		os.makedirs("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/")
	f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/esearch.xml", 'w')
	f.write(output.text)
	f.close()

	#esearch --> parse WebEnv, QueryKey
	tree = parse("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/esearch.xml")
	esearch_root = tree.getroot()

	web = esearch_root.find("WebEnv").text;
	key = esearch_root.find("QueryKey").text;
	count = esearch_root.find("Count").text;

	#print (count);

	#get uilist
	retmax = 5000
	#f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/uilist.text",'a')
	#old_time = os.stat("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/uilist.text").st_mtime
	time_counter = 0
	argv_list = []
	argv_list2 = []
	for i in range(0,int(int(count)/retmax)+1):
		argv_list.append((job_num,i))
	p = Pool(8)
	p.map(worker,argv_list)
	f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/uilist.text",'a')
	print (len(efetch_out_list))
	for elm in efetch_out_list:
		f.write(elm)
	p.close()
	#write all pmid list
	f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/uilist.text", 'r')
	while True:
		line = f.readline().rstrip('\n')
		if len(line) > 0:
			if line[0] == "<":
				curs.close()
				conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
				curs = conn.cursor(pymysql.cursors.DictCursor)
				query = "UPDATE JOB SET TOO_SMALL=1 WHERE J_ID=(%s)"
				curs.execute(query,job_num)
		if not line : break
		if line.isdigit() == False:
			continue
		job_has_pmid.append(int(line))
	f.close()
	step = 500000
	
	for i in range(0,int(int(count)/step)+1):
		argv_list2.append((job_num,i,mysqlId))
	curs.close()
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	p2 = Pool(4)
	p2.map(worker2,argv_list2)
	
	print ("job_has_pmid", len(job_has_pmid))
	print ("new pmid", len(new_pmid))
	temp_exist_pmid = list(set(job_has_pmid) - set(new_pmid))
	for elm in temp_exist_pmid	:
		exist_pmid.append((job_num,elm))	
	#make temp table
	p2.close()
	argv_list3 = []
	for i in range(0,int(int(count)/step)+1):
		argv_list3.append((job_num,i,mysqlId))
	curs.close()
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	p3 = Pool(4)
	p3.map(worker3,argv_list3)

	new_pmid_str = ", ".join(new_pmid)
	#print(new_pmid_str)


	#epost and save new pmids
	epost_param = {'db' : entrez_db, 'id' : new_pmid_str}
	url = base + "epost.fcgi?"
	epost_output = requests.post(url, data=epost_param)
	#print (epost_output.text)
	f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/epost.xml", 'w')
	f.write(epost_output.text)
	f.close()
	curs.close()
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query = "UPDATE JOB SET PMID_COLLECT =2 WHERE J_ID = (%s)"
	curs.execute(query,job_num)      
	if  len(new_pmid) != 0:
		#epost --> parse
		tree = parse("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/epost.xml")                                                       
		epost_root = tree.getroot()                                                  

		web = epost_root.find("WebEnv").text;
		key = epost_root.find("QueryKey").text;                                                         
		#number of thesis to be collected
		#count = int(count) - len(exist_pmid);                                       
		count = len(new_pmid)                                                                             
		print (count);                                                                
																					
		#do efetch and save as xml                                                                                   
		f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/new_pmid_record.xml",'w')  
		f.write("<PubmedArticleSet>")      
		print(int(int(count)/retmax)+1)                                                 
		for i in range(0,int(int(count)/retmax)+1):                                    
			efetch_url = base +"efetch.fcgi?db="+entrez_db+"&WebEnv="+web          
			efetch_url += "&query_key="+key+"&retstart="+str(i*retmax)           
			efetch_url += "&retmax="+str(retmax)+"&rettype=&retmode=xml"  
			while True:
				try:
					efetch_out = requests.get(efetch_url)
				except:
					print("request failed, retry after 5 seconds")
					time.sleep(5)
					continue
				else:
					break
				print (efetch_out.status_code)
				if efetch_out.status_code == 200:
					break
			xmlString = re.sub(r"<\?xml .*\?>", r'', efetch_out.text)
			xmlString = re.sub(r"<\!DOCTYPE .*>", r'', xmlString)
			xmlString = re.sub(r"</PubmedArticleSet>", r'', xmlString)
			xmlString = re.sub(r"<PubmedArticleSet>", r'', xmlString)
			
			#f.write(str(xmlString))                  
			f.write(xmlString.encode('utf-8').strip())         
			
														
		f.write("</PubmedArticleSet>")
		f.close()
		curs.close()
		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		query = "UPDATE JOB SET DO_PMID_INSERT =1 WHERE J_ID = (%s)"
		curs.execute(query,job_num)         
	else:
		
		curs.close()
		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		query = "SELECT COUNT(*) FROM JOB_PMID WHERE J_ID = (%s) ;"
		curs.execute(query,job_num)
		row = curs.fetchone()
		pmid_count = row['COUNT(*)']
		print(pmid_count)
		curs.close()

		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		query = "UPDATE JOB SET PMID_COUNT = (%s) WHERE J_ID = (%s);"
		curs.execute(query,(pmid_count,job_num))
		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		query = "UPDATE JOB SET DO_PMID_INSERT =5 WHERE J_ID = (%s)"
		curs.execute(query,job_num)             
		query = "UPDATE JOB SET WEKA =4 WHERE J_ID = (%s)"
		curs.execute(query,job_num	)              	

