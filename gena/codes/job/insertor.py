import pymysql
import subprocess
import os
import psutil
import sys


def parse_commands(argv):
	from optparse import OptionParser
	parser = OptionParser('"')
	parser.add_option('-i', '--mysqlId', dest='mysqlId')
	options, otherjunk = parser.parse_args(argv)
	return options

if __name__ == '__main__':
	options = parse_commands(sys.argv[1:])
	parser = None
	mysqlId = options.mysqlId
	mysqlIdParam = " "+mysqlId+" "
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query = "SELECT * FROM JOB where DO_PMID_INSERT =1"
	curs.execute(query)
	row = curs.fetchone()

	if row is not None:
		j_id = str(row['J_ID'])
		python_call ="nohup python "
		main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/pmid/pmid_insertor.py "
		std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/insert_pmid_log.out "
		command = ""
		command += python_call
		command += main_dir
		command += j_id
		command += mysqlIdParam
		command += std_out
		print (command)
		query = "UPDATE JOB SET DO_PMID_INSERT =3 WHERE J_ID = (%s)"
		curs.execute(query,j_id)
		status = subprocess.call(command,shell=True)
		if status != 0:
			query = "UPDATE JOB SET DO_PMID_INSERT = -1 WHERE J_ID = (%s)"
			curs.execute(query,j_id)
		query = "SELECT COUNT(*) FROM JOB_PMID WHERE J_ID = (%s) ;"
		curs.execute(query,j_id)
		row = curs.fetchone()
		pmid_count = row['COUNT(*)']
		print(pmid_count)
		curs.close()

		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		query = "UPDATE JOB SET PMID_COUNT = (%s) WHERE J_ID = (%s);"
		curs.execute(query,(pmid_count,j_id))