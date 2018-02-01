import requests
import pymysql
import sys
import os
from xml.etree.ElementTree import parse
from lxml import etree
import re
import time

job_num = sys.argv[1]
mysqlId = sys.argv[2]

conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307)
curs = conn.cursor(pymysql.cursors.DictCursor)

pmid_list = []
job_pmid_list = []
sup_list =[]
des_list = []
qual_list = []
pmid_content_list = []
if os.path.isfile("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/new_pmid_record.xml") is False:
	exit()
context = etree.iterparse("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/new_pmid_record.xml", events=('end',), tag='PubmedArticle')
counter = 0
for event, element in context:
	med_cite = element.find("MedlineCitation")
	pmid = str(int(med_cite.find("PMID").text))
	#print (pmid)
	article = med_cite.find("Article")
	medline = med_cite.find("MedlineJournalInfo")
	title = ""
	country =""
	abstract = ""
	if article is not None:
		if article.find("ArticleTitle").text is not None:
			title = article.find("ArticleTitle").text.encode('utf-8').strip()
		if article.find("Abstract") is not None and \
			article.find("Abstract").find("AbstractText") is not None and \
			article.find("Abstract").find("AbstractText").text is not None:
			abstract = article.find("Abstract").find("AbstractText").text.encode('utf-8').strip()
	if medline is not None:
		if medline.find("Country") is not None:
			country = medline.find("Country").text.encode('utf-8').strip()
	chemical_list = med_cite.find("ChemicalList")
	heading_list = med_cite.find("MeshHeadingList")
	#print (country)
	mesh_list = []
	if chemical_list is not None:
		for child in chemical_list:
			mesh_list.append((child.find("NameOfSubstance").attrib['UI'], "S",pmid))
			if len(child.find("NameOfSubstance").attrib['UI']) > 0:
				if child.find("NameOfSubstance").attrib['UI'][0] == "C":
					sup_list.append((child.find("NameOfSubstance").attrib['UI'], "S",pmid))
				elif child.find("NameOfSubstance").attrib['UI'][0] =="D":
					des_list.append((child.find("NameOfSubstance").attrib['UI'], "S",pmid))
	"""if heading_list is not None:
		for child in heading_list:
			if child.find("DescriptorName") is not None:
				if child.find("DescriptorName").attrib['MajorTopicYN'] == "Y":
					des_list.append((child.find("DescriptorName").attrib['UI'] , child.find("DescriptorName").attrib['MajorTopicYN'],pmid))
			if child.find("QualifierName") is not None:
				if child.find("DescriptorName").attrib['MajorTopicYN'] == "Y":
					qual_list.append((child.find("QualifierName").attrib['UI'], child.find("DescriptorName").attrib['MajorTopicYN'],pmid))"""
	pmid_list.append((pmid,country))
	pmid_content_list.append((pmid, title, abstract))
	job_pmid_list.append((job_num,pmid))
	counter = counter + 1
	if counter  > 100000:
		counter = 0
		curs.close()
		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		query = "INSERT IGNORE INTO PMID (PMID,COUNTRY ) VALUES (%s,%s)"
		curs.executemany(query, pmid_list)
		del pmid_list[:]
		query = "INSERT IGNORE INTO PMID_CONTENT_2 (PMID, TITLE, ABSTRACT) VALUES (%s,%s,%s)"
		curs.executemany(query, pmid_content_list)
		del pmid_content_list[:]
		query	= "INSERT IGNORE INTO PMID_SUP(S_ID, MAJOR,PMID) VALUES	(%s,%s, %s)"
		curs.executemany(query, sup_list)
		del sup_list[:]
		query = "INSERT IGNORE INTO JOB_PMID (J_ID, PMID) VALUES (%s, %s)"
		curs.executemany(query, job_pmid_list)
		del job_pmid_list[:]
	element.clear()
	while element.getprevious() is not None:
    		del element.getparent()[0]
    


if os.path.isfile("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/new_pmid_record.xml") is False:
	exit()
context = etree.iterparse("/home/"+mysqlId+"/Capstone-2017-2/gena/files/"+job_num+"/new_pmid_record.xml", events=('end',), tag='PubmedBookArticle')
for event, element in context:
	med_cite = element.find("BookDocument")
	pmid = str(int(med_cite.find("PMID").text))
	article = med_cite.find("Article")
	medline = med_cite.find("MedlineJournalInfo")
	title = ""
	country =""
	
	if article is not None:
		if article.find("ArticleTitle").text is not None:
			title = article.find("ArticleTitle").text.encode('utf-8').strip()        
	if medline is not None:
		if medline.find("Country") is not None:
			country = medline.find("Country").text.encode('utf-8').strip()  
	chemical_list = med_cite.find("ChemicalList")
	heading_list = med_cite.find("MeshHeadingList")
	mesh_list = []
	if chemical_list is not None:
		for child in chemical_list:
			mesh_list.append((child.find("NameOfSubstance").attrib['UI'], "S",pmid))
			if len(child.find("NameOfSubstance").attrib['UI']) > 0:
				if child.find("NameOfSubstance").attrib['UI'][0] == "C":
					sup_list.append((child.find("NameOfSubstance").attrib['UI'], "S",pmid))
				elif child.find("NameOfSubstance").attrib['UI'][0] =="D":
					des_list.append((child.find("NameOfSubstance").attrib['UI'], "S",pmid))
	"""if heading_list is not None:
		for child in heading_list:
			if child.find("DescriptorName") is not None:
				if child.find("DescriptorName").attrib['MajorTopicYN'] == "Y":
					des_list.append((child.find("DescriptorName").attrib['UI'] , child.find("DescriptorName").attrib['MajorTopicYN'],pmid))
			if child.find("QualifierName") is not None:
				if child.find("DescriptorName").attrib['MajorTopicYN'] == "Y":
					qual_list.append((child.find("QualifierName").attrib['UI'], child.find("DescriptorName").attrib['MajorTopicYN'],pmid))"""
	pmid_list.append((pmid,country))
	pmid_content_list.append((pmid,title))
	job_pmid_list.append((job_num,pmid))
	counter = counter + 1
	if counter  > 100000:
		counter = 0
		curs.close()
		conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
		curs = conn.cursor(pymysql.cursors.DictCursor)
		query = "INSERT IGNORE INTO PMID (PMID,COUNTRY ) VALUES (%s,%s)"
		curs.executemany(query, pmid_list)
		del pmid_list[:]
		query = "INSERT IGNORE INTO PMID_CONTENT_2 (PMID,TITLE ) VALUES (%s,%s)"
		curs.executemany(query, pmid_content_list)
		del pmid_content_list[:]
		query	= "INSERT IGNORE INTO PMID_SUP(S_ID, MAJOR,PMID) VALUES	(%s,%s, %s)"
		curs.executemany(query, sup_list)
		del sup_list[:]
		query = "INSERT IGNORE INTO JOB_PMID (J_ID, PMID) VALUES (%s, %s)"
		curs.executemany(query, job_pmid_list)
		del job_pmid_list[:]
	element.clear()
	while element.getprevious() is not None:
    		del element.getparent()[0]
    


while True:
		try:
			curs.close()
			conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
			curs = conn.cursor(pymysql.cursors.DictCursor)
			query = "INSERT IGNORE INTO PMID (PMID,COUNTRY ) VALUES (%s,%s)"
			curs.executemany(query, pmid_list)
		except:
			continue
		else:
			break
while True:
		try:
			curs.close()
			conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
			curs = conn.cursor(pymysql.cursors.DictCursor)
			query = "INSERT IGNORE INTO PMID_CONTENT_2 (PMID,TITLE ) VALUES (%s,%s)"
			curs.executemany(query, pmid_content_list)
		except:
			continue
		else:
			break
while True:
		try:
			curs.close()
			conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
			curs = conn.cursor(pymysql.cursors.DictCursor)
			query	= "INSERT IGNORE INTO PMID_SUP(S_ID, MAJOR,PMID) VALUES	(%s,%s, %s)"
			curs.executemany(query, sup_list)
		except:
			continue
		else:
			break
while True:
		try:
			curs.close()
			conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
			curs = conn.cursor(pymysql.cursors.DictCursor)
			query = "INSERT IGNORE INTO JOB_PMID (J_ID, PMID) VALUES (%s, %s)"
			curs.executemany(query, job_pmid_list)
		except:
			continue
		else:
			break
while True:
		try:
			curs.close()
			conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
			curs = conn.cursor(pymysql.cursors.DictCursor)
			query = "UPDATE JOB SET DO_PMID_INSERT =5 WHERE J_ID = (%s)"
			curs.execute(query,job_num)
			query = "UPDATE JOB SET WEKA =4 WHERE J_ID = (%s)"
			curs.execute(query,job_num	)             
		except:
			continue
		else:
			break
