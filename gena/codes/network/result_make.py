import sys
import csv
import pymysql
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
j_id = sys.argv[1]
mysqlId = sys.argv[2]


conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

for netId in range(1,5):
    query = "SELECT J_KEY FROM JOB WHERE J_ID = (%s);"
    curs.execute(query,j_id)
    j_key_row = curs.fetchone()

    path = "/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/"
    if netId == 1:
        path += j_key_row['J_KEY']+"_GeneAssociation.csv"
    elif netId == 2:
        path += j_key_row['J_KEY']+"_GeneAssociationSingleNode.csv"
    elif netId == 3:
        path += j_key_row['J_KEY']+"_GeneCoOccurence.csv"
    elif netId == 4:
        path += j_key_row['J_KEY']+"_GeneCoOccurenceSingleNode.csv"

    query = "SELECT * FROM JOB_GENE_3 A, GENE B WHERE J_ID = (%s) AND NET_ID = (%s) AND A.HGNC_ID = B.HGNC_ID ORDER BY DEGREE DESC"
    curs.execute(query,(j_id,netId))
    rows = curs.fetchall()
    count = 0
    f = open(path,'w')
    wr = csv.writer(f)
    wr.writerow(['Symbol','HgncId','Degree','Betweenness','Closeness','Katz'])
    for row in rows:
        wr.writerow([row['SYMBOL'],row['HGNC_ID'],row['Degree'],row['Betweenness'],row['Closeness'],row['Katz']])
        count = count + 1
    f.close()
    
    if netId == 1:
        query = "UPDATE JOB SET GENE_NUM_ASSO = (%s) WHERE J_ID = (%s)"
    elif netId == 2:
        query = "UPDATE JOB SET GENE_NUM_ASSO_NODE = (%s)  WHERE J_ID = (%s)"
    elif netId == 3:
        query = "UPDATE JOB SET GENE_NUM_COOC = (%s)  WHERE J_ID = (%s)"
    elif netId == 4:
        query = "UPDATE JOB SET GENE_NUM_COOC_NODE = (%s)  WHERE J_ID = (%s)"
    curs.execute(query,(count,j_id))
    


query = "UPDATE JOB SET JOB_DONE_TIME = NOW() WHERE J_ID = (%s)"
curs.execute(query,j_id)
query = "SELECT EMAIL,J_KEY FROM JOB WHERE J_ID = (%s);"
curs.execute(query,j_id)


query = "SELECT * FROM JOB WHERE J_ID = (%s);"
curs.execute(query,j_id)

try:
    row = curs.fetchone()
    if(row['EMAIL'] != "" and row['EMAIL'] is not None and row['EMAIL']!="undefined"):
        StartDate = row['START_DATE'].strftime('%Y-%m-%d')
        EndDate = row['END_DATE'].strftime('%Y-%m-%d')
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS
        smtp.login('genaxity@gmail.com', 'bio53295')
        #smtp.login('bcb225@gmail.com', 'qkdckdqo1!')
        msg = MIMEText(
        "Dear GENAX user.\n\n\n"
		"This is Genaxity, the administrator of GENAX.\n\n"
        "Your job has been completed.\n\n"
        "Search Query : "+row['QUERY']+"\n\n"
        "Search Start Date : "+StartDate+"\n\n"
        "Search End Date : "+EndDate+"\n\n"
        "This is the link to access your job status and result.\n"
        "http://genax.tools/#/result/"+row['J_KEY']+"\n\n"
        "Thank you for waiting for the GENAX result.\n\n\n"
        "Sincerely.\n"
        "Genaxity"
        )
        msg['Subject'] = '[GENAX] Your job has been completed.'
        msg['To'] = row['EMAIL']
        #smtp.sendmail('bcb225@gmail.com', 'indigenmaster@gmail.com', msg.as_string())
        smtp.sendmail('genaxity@gmail.com', row['EMAIL'], msg.as_string())
except:
    pass
query = "UPDATE JOB SET NETWORK = 6 WHERE J_ID = (%s)"
curs.execute(query,j_id)