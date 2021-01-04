# import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
import csv
import os
import string
import re
import logging
import json
import pandas as pd
import pygsheets
import urllib
from itertools import islice
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from datetime import datetime,timedelta,date
import random


import smtplib
from oauth2client.service_account import ServiceAccountCredentials
import mimetypes
from email.encoders import encode_base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from scraping_lib import *

logging.basicConfig(filename='tkb.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

def create_message(from_addr, to_addrs, mime):
    try:
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        if True:
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login("riza.pratama@shopee.com", 'fwbaqeahajlofvzi')
        mailServer.sendmail(from_addr, to_addrs, mime.as_string())
        mailServer.close()
    except:
        traceback.print_exc()
        return False
    return True

def get_attachment(attachment_file_path):
    content_type, encoding = mimetypes.guess_type(attachment_file_path)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    file = open(attachment_file_path, 'rb')
    if main_type == 'text':
        attachment = MIMEText(file.read())
    elif main_type == 'message':
        attachment = email.message_from_file(file)
    elif main_type == 'image':
        attachment = MIMEImage(file.read(),_sub_type=sub_type)
    elif main_type == 'audio':
        attachment = MIMEAudio(file.read(),_sub_type=sub_type)
    else:
        attachment = MIMEBase(main_type, sub_type)
        attachment.set_payload(file.read())
        encode_base64(attachment)
    file.close()
    attachment.add_header(
        'Content-Disposition', 
        'attachment',     
        filename=os.path.basename(attachment_file_path)
    )
    print(os.path.basename(attachment_file_path))
    return attachment    

def send_mail(subject, msg, from_addr, to_addrs, cc_addrs=[], bcc_addrs=[], attachments=[], func=create_message, *a, **b):

    mime = MIMEMultipart()

    mime['From'] = from_addr
    mime['To'] = ', '.join(to_addrs)
    #mime['To'] = to_addrs
    if len(cc_addrs) > 0:
        mime['Cc'] = ', '.join(cc_addrs)

    mime['Subject'] = subject
    body = MIMEText(msg, _subtype='html', _charset='utf-8')
    mime.attach(body)

    for file_name in attachments:
        mime.attach(get_attachment(file_name))

    _to_addrs = to_addrs + cc_addrs + bcc_addrs
    result = func(from_addr, _to_addrs, mime)

# Sending auto email
def compile(attachments, to_addrs):
    from_addr = 'Shopee ID - DATA Team'
    # to_addrs = ['riza.pratama@shopee.com']
    cc_addrs = []
    # cc_addrs = ['riza.pratama@shopee.com']
    # cc_addrs = []
    bcc_addrs = []
    subject = 'Scraping - Daily TKB (%s)' % (datetime.now().strftime('%Y%m%d '))
    msg = 'Hi all,<br><br>' \
        'Please find the report attached.<br>'\
        'Should you have any questions, please contact Riza (riza.pratama@shopee.com).<br><br>'\
        'Thanks.'
    #attachments = []
    send_mail(subject, msg, from_addr, to_addrs, cc_addrs, bcc_addrs, attachments)

def scrape_tkb(url):
	if 'investree' in url:
		try:
			tkb=scrape_investree(url)
		except Exception as e:
			logger.error(e)
			tkb=''
		source='investree'
	elif 'taralite' in url:
		try:
			tkb=scrape_taralite(url)
		except Exception as e:
			logger.error(e)
			tkb=''
		source='taralite'
	elif 'findaya' in url:
		try:
			tkb=scrape_findaya(url)
		except Exception as e:
			logger.error(e)
			tkb=''
		source='findaya'
	elif 'amartha' in url:
		try:
			tkb=scrape_amartha(url)
		except Exception as e:
			logger.error(e)
			tkb=''
		source='amartha'
	elif 'danamas' in url:
		try:
			tkb=scrape_danamas(url)
		except Exception as e:
			logger.error(e)
			tkb=''
		source='danamas'
	elif 'modalku' in url:
		try:
			tkb=scrape_modalku(url)
		except Exception as e:
			logger.error(e)
			tkb=''
		source='modalku'
	else:
		tkb=''
		source=''
	return tkb,source

def scrape_investree(url):
	soup=scrape_selenium_lite2(url)
	tkb_raw=soup.find('span',class_='tkb-num').text.replace(',','.').replace('\n','').replace(' ','')
	# print(tkb_raw)
	tkb=tkb_raw
	return tkb

def scrape_taralite(url):
	soup=scrape_selenium_lite2(url)
	tkb_raw=soup.find('div',class_='inline-data').text.replace(',','.').replace('\n','').replace(' ','').replace('TKB90:','')
	# print(tkb_raw)
	tkb=tkb_raw
	return tkb

def scrape_findaya(url):
	soup=scrape_selenium_lite(url)
	tkb_raw=soup.find('div',class_='col-auto menu-highlight').text.replace(',','.').replace('\n','').replace(' ','').replace('TKB90:','')
	# print(tkb_raw)
	tkb=tkb_raw
	return tkb

def scrape_amartha(url):
	soup=scrape_selenium_lite(url)
	tkb_raw=soup.find('span',id='installmentsOnTime').text.replace(',','.').replace('\n','').replace(' ','')
	# print(tkb_raw)
	tkb=tkb_raw
	return tkb

def scrape_danamas(url):
	soup=scrape_selenium_lite(url)
	tkb_raw=soup.find('div',class_='textnilai').text.replace(',','.').replace('\n','').replace('\t','').replace(' ','').replace('TKB=','')
	# print(tkb_raw)
	tkb=tkb_raw
	return tkb

def scrape_modalku(url):
	soup=scrape_selenium_lite2(url)
	tkb_raw=soup.find('div',class_='statistic').find('p',class_='Gilroy-SemiBold number').text.replace(',','.').replace('\n','').replace(' ','')
	# print(tkb_raw)
	tkb=tkb_raw
	return tkb

urls=[
	'https://investree.id/',
	'https://www.taralite.com/',
	'https://www.findaya.com/',
	'https://amartha.com/id_ID/',
	'https://www.danamas.co.id/web/HomeAction_home.action',
	'https://modalku.co.id/'
]

results=[]
for url in urls:
	tkb=''
	retry=5
	while tkb=='' and retry>0:
		tkb,source=scrape_tkb(url)
		# print(tkb,source)
		result = {
				  'source':source,
				  'url':url,
				  'tkb':tkb,
				  'scraped_date':datetime.now()
		}
		# print(result)

		if tkb!='':
			retry=0
		else:
			retry=retry-1
	results.append(result)
print(results)

csv_filename='tkb.csv'
results_df=pd.DataFrame(results)
results_df = results_df[['source','url','tkb','scraped_date']]  
results_df.to_csv(csv_filename,index=False, encoding='utf8')
print('csv ok')

email_recipient_list=['riza.pratama@shopee.com']
compile([csv_filename], email_recipient_list)

api_endpoint = 'https://autoingestion.idata.shopeemobile.com/api/v1/csv/upload'
headers={'Authorization': 'Bearer b4df0f85d8f1587c5b542b32fcb3e654'}
response = requests.post(api_endpoint, headers=headers, files={'csv': open(csv_filename, 'rb')})
