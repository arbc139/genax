import requests
import time
import random
import smtplib
from email.mime.text import MIMEText
from lxml import etree

url = 'https://www2.yonsei.ac.kr/entrance/2018/medi/pass2018_med_1st/pass.asp'
#url = 'https://www2.yonsei.ac.kr/entrance/2017/medi/pass2017_med_1st/pass.asp'
url = 'http://admission.yonsei.ac.kr/seoul/admission/html/counsel/notice.asp?s_type=TYPE67'
yonsei = requests.get(url)
old_html = yonsei.text
while True:
	yonsei = requests.get(url)
	sec = random.randrange(5,10)
	print(sec,yonsei.status_code)
	new_html = yonsei.text
	if old_html == new_html:
		print("Not Yet")
	else:
		print("Updated")
		smtp = smtplib.SMTP('smtp.gmail.com', 587)
	        smtp.ehlo()      # say Hello
	        smtp.starttls()  # TLS
	        smtp.login('genaxity@gmail.com', 'bio53295')
	        msg = MIMEText(
	        "Yonsei Medical School 1st Admission Announced.\n\n"
		"Check Your Result.\n\n"
		"Good Luck!\n\n"
		"https://www2.yonsei.ac.kr/entrance/2018/medi/pass2018_med_1st/pass.asp\n"
	        )
	        msg['Subject'] = 'Yonsei Medical School 1st Admission Announced.'
	        smtp.sendmail('genaxity@gmail.com', 'bcb225@gmail.com', msg.as_string())
	time.sleep(sec)