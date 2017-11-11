import subprocess
import sys
import pymysql
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)

j_id = sys.argv[1]
mysqlId = sys.argv[2]
query = "SELECT * FROM JOB WHERE J_ID = (%s)"
curs.execute(query,j_id)

row = curs.fetchone()

#java_call =" java -cp /home/"+mysqlId+"/Capstone-2017-2/gena/weka-3-8-1/weka.jar  -Xms30000m -Xmx50000m "
#java_call =" java -cp /home/"+mysqlId+"/Capstone-2017-2/gena/weka-3-8-1/weka.jar -Xms10000m -Xmx15000m "
#java_call =" java -cp /home/"+mysqlId+"/Capstone-2017-2/gena/weka-3-8-1/weka.jar -Xms10000m -Xmx30000m "
#java_call =" java -cp /home/"+mysqlId+"/Capstone-2017-2/gena/weka-3-8-1/weka.jar -Xmx30000m "
java_call =" java -cp /home/"+mysqlId+"/Capstone-2017-2/gena/weka-3-8-1/weka.jar -Xmx58000m "
weka_dir = "  weka.associations.FPGrowth -t "
#weka_dir = "  weka.associations.Apriori -t "  #for yearly test
arff_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/input.arff "


num_rule =" -N "+str(row['N'])+" "
#num_rule =" -N 1000000000 "

#min_metric = " -C 0.0001"
#min_metric = " -C 0.01" # for yearly test
min_metric = " -C "+str(row['C'])+" "

#upper_bound_min_supp=" -U 100 "
#upper_bound_min_supp=" -U 1 "
upper_bound_min_supp=" -U "+str(row['U'])+" "

#lower_bound_min_supp=" -M 0.001 "
#lower_bound_min_supp=" -M 0.001 " #test 1
#lower_bound_min_supp=" -M 0.00001 " #test 2
lower_bound_min_supp=" -M "+str(row['M'])+" "


#delta_mun_supp=" -D 0.5"
#delta_mun_supp=" -D 0.05"
delta_mun_supp=" -D "+str(row['D'])+" "
#delta_mun_supp=" -D 0.05 -S -1.0 -c -1"

#index_pos_val =" -P "+str(row['P'])+" "

max_items =" -I "+str(row['I'])+" "

metric =" -T "+str(row['T'])+" "

if row['S'] is 'TRUE':
    option_s = " -S "
else :
    option_s = ""


std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/"+j_id+"/asso.out "
command = ""
command += java_call
command += weka_dir
command += arff_dir
command += num_rule
command += min_metric
command += upper_bound_min_supp
command += lower_bound_min_supp
command += delta_mun_supp
#command += index_pos_val
command += max_items
command += metric
command += option_s
command += std_out
subprocess.call(command,shell=True)

query = "UPDATE JOB SET WEKA =4 WHERE J_ID = (%s)"
curs.close()
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8') 
curs = conn.cursor(pymysql.cursors.DictCursor)
curs.execute(query,j_id)      