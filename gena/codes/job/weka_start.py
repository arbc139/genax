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
	conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3306) 
	curs = conn.cursor(pymysql.cursors.DictCursor)
	query = "SELECT * FROM JOB where PMID_COLLECT=2 AND DO_PMID_INSERT =5 AND WEKA = 0"
	curs.execute(query)
	row = curs.fetchone()
	if row is not None:
		j_id = str(row['J_ID'])
		python_call ="nohup python "
		main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/arff_make.py "
		std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/arff_make_log.out "
		command = ""
		command += python_call
		command += main_dir
		command += j_id
		command += mysqlIdParam
		command += std_out
		print (command)

		for proc in psutil.process_iter():
			cmdlist = set(proc.cmdline())
			if command in cmdlist:
				print(command,"\nIt is killed because there exists same job.\n")
				exit()

		query = "UPDATE JOB SET WEKA =1 WHERE J_ID = (%s)"
		curs.execute(query,j_id)
		status = subprocess.call(command,shell=True)
		if status != 0:
			query = "UPDATE JOB SET WEKA = -1 WHERE J_ID = (%s)"
			curs.execute(query,j_id)


	query = "SELECT * FROM JOB where PMID_COLLECT=2 AND DO_PMID_INSERT =5 AND WEKA = 2"
	curs.execute(query)
	rows = curs.fetchall()
	temp_j_id = "99999999999999999999999"
	for row in rows:
		j_id = row['J_ID']
		if int(temp_j_id) > int(j_id):
			temp_j_id = j_id

	if row is not None:
		j_id = str(temp_j_id)
		arff_size = os.path.getsize("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/input.arff")
		if arff_size > 18000000000:
			query = "UPDATE JOB SET WEKA = 4 WHERE J_ID = (%s)"
			curs.execute(query,j_id)
			exit()

		query = "SELECT * FROM JOB_LOG where STATUS = 1"
		curs.execute(query)
		rows = curs.fetchall()
		arff_total = arff_size
		for row in rows:
			arff_total = arff_total + int(row['ARFF'])
			if arff_total > 18000000000:
				print("Job "+j_id+" waiting because there are not enough memory.")
				exit()

		python_call ="nohup python "
		main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/weka/weka_run.py "
		std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/weka_run_log.out "
		command = ""
		command += python_call
		command += main_dir
		command += j_id
		command += mysqlIdParam
		command += std_out

		for proc in psutil.process_iter():
			cmdlist = set(proc.cmdline())
			if command in cmdlist:
				print(command,"\nIt is killed because there exists same job.\n")
				exit()

		query = "UPDATE JOB SET WEKA =3 WHERE J_ID = (%s)"
		curs.execute(query,j_id)

		query = "UPDATE JOB_LOG SET ARFF = (%s) WHERE J_ID = (%s)"
		curs.execute(query,(arff_size,j_id))
		
		
		print (command)
		status = subprocess.call(command,shell=True)
		if status != 0:
			query = "UPDATE JOB SET WEKA = -2 WHERE J_ID = (%s)"
			curs.execute(query,j_id)
