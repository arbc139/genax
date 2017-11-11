import sys
import pymysql
import re
j_id = sys.argv[1]
j_key = sys.argv[2]

filename = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_edgeCooc.csv"
net_asso = open(filename,'r')
csv_write_list = []
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
lines = net_asso.readlines()
for line in lines:
    line_list = line.split(",")
    
    query = "SELECT SYMBOL FROM GENE WHERE HGNC_ID = (%s)"
    curs.execute(query,line_list[1])
    row = curs.fetchone()
    if row is None:
        continue
    elm1 = row['SYMBOL']

    curs.execute(query,line_list[2])
    row = curs.fetchone()
    if row is None:
        continue
    elm2 = row['SYMBOL']

    csv_write_list.append((elm1,elm2,line_list[3]))
    #print (csv_write_list)
    print (line_list,line_list[1],line_list[2], line_list[3])


filename_2 = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"+j_key+"_edgeCoocProcessed.csv"
net_asso_2 = open(filename_2,'w')
net_asso_2.write("Type,Source,Target,Weight\r\n")
for elm in csv_write_list:
    net_asso_2.write("Undirected,"+elm[0]+","+elm[1]+","+elm[2])

