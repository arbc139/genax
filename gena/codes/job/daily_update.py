import pymysql
import os
# Import smtplib for the actual sending function
import sys
# Import the email modules we'll need

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

	query = "DELETE FROM GENE_PMID"
	curs.execute(query)

	query = "DELETE FROM JOB_COUNTRY"
	curs.execute(query)

	query = "DELETE FROM JOB_GENE_2"
	curs.execute(query)

	query = "DELETE FROM JOB_GENE_3"
	curs.execute(query)

	query = "DELETE FROM JOB_LOG"
	curs.execute(query)

	query = "DELETE FROM JOB_PMID"
	curs.execute(query)

	query = "DELETE FROM JOB"
	curs.execute(query)

	curs.close()
	conn.close()
