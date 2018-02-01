import pymysql
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3306) 
curs = conn.cursor(pymysql.cursors.DictCursor)
query = "CREATE TEMPORARY TABLE temp_uilist_1 (pmid int(11));"
curs.execute(query)
