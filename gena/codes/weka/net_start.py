import pymysql
import subprocess
import os
import sys
mysqlId = sys.argv[1]
mysqlIdParam  = " "+mysqlId+" "
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3306) 
curs = conn.cursor(pymysql.cursors.DictCursor)
query = "SELECT * FROM JOB where WEKA = 4"
curs.execute(query)
row = curs.fetchone()
if row is not None:
	j_id = str(row['J_ID'])
	python_call ="nohup python "
	main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/weka_analysis.py "
	std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/weka_analysis_log.out "
	command = ""
	command += python_call
	command += main_dir
	command += j_id
	command += mysqlIdParam
	command += std_out
	print (command)
	query = "UPDATE JOB SET NETWORK = 1 WHERE J_ID = (%s)"
	curs.execute(query,j_id)
	subprocess.call(command,shell=True)
