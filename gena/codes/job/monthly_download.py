import requests
import sys
import os
from xml.etree.ElementTree import parse
from lxml import etree
import re
import time
import datetime
import time
import subprocess

child_num = sys.argv[1]
mysqlId = sys.argv[2]
mysqlIdParam = " "+mysqlId+" "
entrez_db = 'pubmed'

query_string = ""
now = datetime.datetime.now()
nowDate = now.strftime('%Y/%m/%d')
job_num = str(nowDate)

endDatetime = now + datetime.timedelta(days=(-19*(int(child_num)-1)))
endDate = endDatetime.strftime('%Y/%m/%d')
oldDatetime = now + datetime.timedelta(days=(-19*int(child_num))+1)
oldDate = oldDatetime.strftime('%Y/%m/%d')


period = "((\""+str(oldDate)+"\"[Date - Entrez] : \""+str(endDate)+"\"[Date - Entrez]))"
query_string += period
#assemble the esearch URL
base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
url = base + "esearch.fcgi?db="+entrez_db+"&term="+query_string+"&usehistory=y&api_key=5b1bbe2ef2a0bebe85a9937c9d71e9085f09";

#do esearch
output = requests.get(url)

#save esearch result
if not os.path.exists("/home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+child_num+"/"):
    os.makedirs("/home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+child_num+"/")
f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+child_num+"/esearch.xml", 'w')
f.write(output.text)
f.close()

#esearch --> parse WebEnv, QueryKey
tree = parse("/home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+child_num+"/esearch.xml")
esearch_root = tree.getroot()

web = esearch_root.find("WebEnv").text;
key = esearch_root.find("QueryKey").text;
count = esearch_root.find("Count").text;
retmax = 5000                                                             
f = open("/home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+child_num+"/new_pmid_record.xml",'w')  
f.write("<PubmedArticleSet>")      
print(int(int(count)/retmax)+1)                                                 
for i in range(0,int(int(count)/retmax)+1):                                    
    efetch_url = base +"efetch.fcgi?db="+entrez_db+"&WebEnv="+web          
    efetch_url += "&query_key="+key+"&retstart="+str(i*retmax)           
    efetch_url += "&retmax="+str(retmax)+"&rettype=&retmode=xml&api_key=5b1bbe2ef2a0bebe85a9937c9d71e9085f09"  
    while True:
        try:
            efetch_out = requests.get(efetch_url)
        except:
            print("request failed, retry after 5 seconds")
            time.sleep(5)
            continue
        else:
            break
        print (efetch_out.status_code)
        if efetch_out.status_code == 200:
            break
    xmlString = re.sub(r"<\?xml .*\?>", r'', efetch_out.text)
    xmlString = re.sub(r"<\!DOCTYPE .*>", r'', xmlString)
    xmlString = re.sub(r"</PubmedArticleSet>", r'', xmlString)
    xmlString = re.sub(r"<PubmedArticleSet>", r'', xmlString)
    
    #f.write(str(xmlString))                  
    f.write(xmlString.encode('utf-8').strip())         
    
                                                    
f.write("</PubmedArticleSet>")
f.close()

python_call ="nohup python "
main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/job/monthly_insert.py "
std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+child_num+"/monthly_insert_log.out "
command = ""
command += python_call
command += main_dir
command += job_num
command += mysqlIdParam
command += " "
command += child_num
command += std_out
print (command)
subprocess.call(command,shell=True)
