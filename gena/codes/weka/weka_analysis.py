import subprocess
import sys
import pymysql
import os

j_id = sys.argv[1]
mysqlId = sys.argv[2]
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

mysqlIdParam = " "+mysqlId+" "
query = "SELECT J_KEY FROM JOB WHERE J_ID = (%s)"
curs.execute(query,j_id)
j_key = curs.fetchone()


if not os.path.exists("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key['J_KEY']+"_edgeAsso.csv"):
    os.mknod("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key['J_KEY']+"_edgeAsso.csv")


query = "INSERT INTO GENE_PMID(J_ID,HGNC_ID,PMID) SELECT A.J_ID, D.HGNC_ID, A.PMID FROM JOB_PMID A, PMID B, PMID_SUP C, SUP D, GENE E WHERE A.J_ID = (%s) AND E.HGNC_ID != 'N/A' AND A.PMID = B.PMID AND B.PMID = C.PMID AND C.S_ID = D.S_ID AND D.HGNC_ID = E.HGNC_ID;"
curs.execute(query,j_id)
python_call ="nohup python "
main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/weka_analysis/FPGrowth/main.py "
#main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/weka_analysis/Apriori/main.py "
input_dir = " -i /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/asso.out "
output_dir =" -o /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key['J_KEY']+"_edgeAsso.csv "
job_option =" -d "+j_id+ " "
mysql_option =" -md "+mysqlId+ " "
std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/net_asso_log.out "
command = ""
command += python_call
command += main_dir
command += input_dir
command += output_dir
command += job_option	
command += mysql_option
command += std_out
status = subprocess.call(command,shell=True)

python_call ="nohup python "
#main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/cooc.py "
main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/test_cooc.py "
std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/net_cooc_log.out "
command = ""
command += python_call
command += main_dir
command += j_id
command += mysqlIdParam
command += std_out
status = subprocess.call(command,shell=True)
if status != 0:
	query = "UPDATE JOB SET NETWORK = -4 WHERE J_ID = (%s)"
	curs.execute(query,j_id)
	query = "UPDATE JOB_LOG SET STATUS = -1 WHERE J_ID = (%s)"
	curs.execute(query,j_id)
"""
python_call ="nohup python "
main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/des_counter.py "
std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/des_counter_log.out "
command = ""
command += python_call
command += main_dir
command += j_id
command += std_out
subprocess.call(command,shell=True)
"""

query = "UPDATE JOB SET NETWORK = 2 WHERE J_ID = (%s)"
curs.execute(query,j_id)
