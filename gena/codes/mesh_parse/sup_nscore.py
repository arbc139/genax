import pymysql
import requests
from xml.etree import ElementTree
import time
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
curs = conn.cursor(pymysql.cursors.DictCursor)

query = "UPDATE SUP SET N_SCORE =0 WHERE N_SCORE = -1"
curs.execute(query)
