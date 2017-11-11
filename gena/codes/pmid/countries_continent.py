import subprocess
import sys
import pymysql
import xlrd

conn = pymysql.connect(autocommit ='True', host='localhost', user='', password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

workbook = xlrd.open_workbook('countries.xls')
worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows
 
row_val = []
for row_num in range(nrows):
    row_val.append(worksheet.row_values(row_num))    
#print (row_val)
for row in row_val:
    query = "UPDATE COUNTRY SET AREA = (%s) WHERE C_NAME = (%s)"
    curs.execute(query,(row[1],row[0]))      
