import re
import pymysql
import csv
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

with open('/home/"+mysqlId+"/Capstone-2017-2/gena/meshfile/CTD_pathways.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',') 
	for row in reader:
		query = "INSERT INTO PATHWAY(P_NAME) VALUES ((%s))"
		if(row[0][0]=="#"):
			continue
		curs.execute(query, row[0])
		print (row[0])
