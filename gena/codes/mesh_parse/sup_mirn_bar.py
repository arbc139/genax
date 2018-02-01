import pymysql
import re
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
curs = conn.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM SUP WHERE S_NAME REGEXP 'MIRN-';"
curs.execute(query)
rows = curs.fetchall()
for row in rows:
	original = row['PROCESSED']
	processed = re.sub(r"-", r'', original)
	query = "UPDATE SUP SET PROCESSED = (%s) WHERE S_ID = (%s)"
	curs.execute(query,(processed, row['S_ID']))
