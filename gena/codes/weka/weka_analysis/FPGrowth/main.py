
from csv_manager import CsvManager
from weka_manager import WekaManager
from weka_parser import WekaParser
import sys
import pymysql

def parse_commands(argv):
  from optparse import OptionParser
  parser = OptionParser('"')
  parser.add_option('-i', '--inputFile', dest='input_file')
  parser.add_option('-o', '--outputFile', dest='output_file')
  parser.add_option('-d', '--id', dest='job_id')
  options, otherjunk = parser.parse_args(argv)
  return options

try:
  options = parse_commands(sys.argv[1:])

  parser = None
  weka_objects = None
  with open(options.input_file, 'r') as weka_file:
    parser = WekaParser(weka_file)
    weka_objects = parser.parse()

  weka_manager = WekaManager(weka_objects)
  weka_manager.filter_objects()
  # weka_manager.normalize()

  conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
  curs = conn.cursor(pymysql.cursors.DictCursor)
  query = "SELECT EM FROM JOB WHERE J_ID = (%s) ;"
  curs.execute(query ,options.job_id)

  row = curs.fetchone()

  edgeMetric = row['EM']
except:
  pass
try:
  analyze_result = weka_manager.analyze(edgeMetric)
  analyze_result = weka_manager.normalize_weights(analyze_result)
except:
  pass
counter = 0


with open(options.output_file, 'w+') as out_file:
  out_file.write("HgncId,HgncId,Weight\n")
  try:
    for relationship, weight in analyze_result.items():
      out_str = ""
      out_str += relationship[0]+","+relationship[1]+","+str(weight)+"\n"
      #print (out_str)
      counter = counter + 1
      out_file.write(out_str)
  except:
    pass
conn = pymysql.connect(autocommit ='True', host='localhost', user=mysqlId, password='',db='HUBMED', charset='utf8', port=3307) 
curs = conn.cursor(pymysql.cursors.DictCursor)
query = "UPDATE JOB SET EDGE_NUM_ASSO = (%s) WHERE J_ID = (%s) ;"
curs.execute(query ,(counter,options.job_id))
