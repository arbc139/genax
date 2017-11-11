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
import multiprocessing

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
    entrez_db = 'pubmed'

    query_string = ""
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y/%m/%d')
    job_num = str(nowDate)

    def worker(child_num):
        if not os.path.exists("/home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+str(child_num)+"/"):
            os.makedirs("/home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+str(child_num)+"/")
        python_call ="nohup python "
        main_dir = " /home/"+mysqlId+"/Capstone-2017-2/gena/codes/job/monthly_download.py "
        std_out = " > /home/"+mysqlId+"/Capstone-2017-2/gena/files/monthly/"+job_num+"/"+str(child_num)+"/monthly_insert_log.out "
        command = ""
        command += python_call
        command += main_dir
        command += str(child_num)
        command += mysqlIdParam
        command += std_out
        print (command)
        subprocess.call(command,shell=True)
        return

    if __name__ == '__main__':
        jobs = []
        for i in range(1,11):
            p = multiprocessing.Process(target=worker, args=(i,))
            jobs.append(p)
            p.start()