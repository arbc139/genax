import pymysql
import subprocess
import os
# Import smtplib for the actual sending function
import smtplib
import sys
# Import the email modules we'll need
from email.mime.text import MIMEText

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
	query = "UPDATE JOB_LOG SET STATUS = -1 WHERE J_ID IN (SELECT J_ID FROM JOB WHERE PMID_COLLECT < 0 OR DO_PMID_INSERT < 0 OR WEKA < 0 OR NETWORK < 0);"
	curs.execute(query)



	query = "SELECT COUNT(*) FROM JOB_LOG WHERE STATUS = 1"
	curs.execute(query)
	row = curs.fetchone()
	#if row['COUNT(*)'] > 3:#Num of job that can be done in one cycle is 4


	if row['COUNT(*)'] > 0:  #Num of job that can be done in one cycle is 1
		exit()


	query = "SELECT * FROM JOB where PMID_COLLECT =0"
	curs.execute(query)
	row = curs.fetchone()

	if row is not None:
		j_id = str(row['J_ID'])
		mysqlIdParam = " "+mysqlId+" "
		query = "INSERT INTO JOB_LOG(J_ID, STATUS) VALUES ((%s),(%s))"
		curs.execute(query,(j_id,1))
		query = "UPDATE JOB SET PMID_COLLECT =1 WHERE J_ID = (%s)"
		curs.execute(query,j_id)
		if not os.path.exists("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"):
			os.makedirs("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/")
		python_call ="nohup python "
		main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/pmid/get_pmid_test.py "
		std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/get_pmid_log.out "
		command = ""
		command += python_call
		command += main_dir
		command += j_id
		command += mysqlIdParam
		command += std_out
		print (command)
		query = "UPDATE JOB SET JOB_START_TIME = NOW() WHERE J_ID = (%s)"
		curs.execute(query,j_id)
		#print ("email:",row['EMAIL'])
		try :
			if(row['EMAIL'] != "" and row['EMAIL'] is not None and row['EMAIL']!="undefined"):
				StartDate = row['START_DATE'].strftime('%Y-%m-%d')
				EndDate = row['END_DATE'].strftime('%Y-%m-%d')
				smtp = smtplib.SMTP('smtp.gmail.com', 587)
				smtp.ehlo()      # say Hello
				smtp.starttls()  # TLS
				smtp.login('genaxity@gmail.com', 'bio53295')
				#smtp.login('bcb225@gmail.com', 'qkdckdqo1!') 
				msg = MIMEText("Dear GENAX user.\n\n\n"
				"This is Genaxity, the administrator of GENAX.\n\n"
				"Your job has been started.\n\n"
				"Search Query : "+row['QUERY']+"\n\n"
				"Search Start Date : "+StartDate+"\n\n"
				"Search End Date : "+EndDate+"\n\n"
				"This is the link to access your job status and result.\n"
				"http://genax.tools/#/result/"+row['J_KEY']+"\n\n"
				"As soon as the job completes, an e-mail will be delivered to you again.\n\n"
				"Thank you for using our service.\n\n\n"
				"Sincerely.\n"
				"Genaxity")
				msg['Subject'] = '[GENAX] Your job has been started.'
				msg['To'] = row['EMAIL']
				#smtp.sendmail('bcb225@gmail.com', 'indigenmaster@gmail.com', msg.as_string())
				smtp.sendmail('genaxity@gmail.com', row['EMAIL'], msg.as_string())
		except:
			pass


		status = subprocess.call(command,shell=True)
		if status != 0:
			query = "UPDATE JOB SET PMID_COLLECT = -1 WHERE J_ID = (%s)"
			curs.execute(query,j_id)