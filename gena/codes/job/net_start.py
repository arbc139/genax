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

	query = "SELECT * FROM JOB where WEKA = 4 AND NETWORK = 0"
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
		for proc in psutil.process_iter():
			cmdlist = set(proc.cmdline())
			if command in cmdlist:
				print(command,"\nIt is killed because there exists same job.\n")
				exit()
		query = "UPDATE JOB SET NETWORK = 1 WHERE J_ID = (%s)"
		curs.execute(query,j_id)
		status = subprocess.call(command,shell=True)
		if status != 0:
			query = "UPDATE JOB SET NETWORK = -1 WHERE J_ID = (%s)"
			curs.execute(query,j_id)
	query = "SELECT * FROM JOB where NETWORK = 2"
	curs.execute(query)
	row = curs.fetchone()
	if row is not None:
		j_id = str(row['J_ID'])

		query = "UPDATE JOB SET WEKA = 5 WHERE J_ID = (%s)"
		curs.execute(query,j_id)

		python_call ="nohup python "
		main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/network/net_test.py "
		std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/net_test.out "
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
		query = "UPDATE JOB SET NETWORK = 3 WHERE J_ID = (%s)"
		curs.execute(query,j_id)
		status = subprocess.call(command,shell=True)
		if status != 0:
			query = "UPDATE JOB SET NETWORK = -2 WHERE J_ID = (%s)"
			curs.execute(query,j_id)

	query = "SELECT * FROM JOB where NETWORK = 4"
	curs.execute(query)
	row = curs.fetchone()
	if row is not None:
		j_id = str(row['J_ID'])
		python_call ="nohup python "
		main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/network/result_make.py "
		std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/result_make_log.out "
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
		query = "UPDATE JOB SET NETWORK = 5 WHERE J_ID = (%s)"
		curs.execute(query,j_id)
		status = subprocess.call(command,shell=True)
		if status != 0:
			query = "UPDATE JOB SET NETWORK = -3 WHERE J_ID = (%s)"
			curs.execute(query,j_id)
