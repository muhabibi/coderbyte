#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import csv
import copy
import datetime
import random
from threading import Thread
import smtplib
import mimetypes
import string
import os
import os.path
import traceback
import pprint
from urllib.request import urlopen as uReq
import urllib.parse
from urllib.error import *
import http.client
from bs4 import BeautifulSoup
import math
import calendar
import time
import logging
import pandas as pd
from itertools import islice
from pathlib import Path
from datetime import datetime
import json
import urllib
from bs4 import NavigableString as nav
import re
from time import sleep
import random
import pyautogui

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def scrape_urllib(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req,timeout=10)
    page_html = response.read()
    response.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    return page_soup

def scrape_urllib_netnut(url):
    countries=['sg','in','kr','us']
    country=countries[random.randint(0,len(countries)-1)]
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    # proxy = urllib.request.ProxyHandler({'https': 'http://shopee-cc-any:fDCqZWu2@gw.ntnt.io:5959'})
    proxy = urllib.request.ProxyHandler({'https': 'http://shopee-cc-'+country+':fDCqZWu2@gw.ntnt.io:5959'})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url,timeout=10)
    page_html = response.read()
    response.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    return page_soup

def scrape_requests(url):
    user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
    response  = requests.get(url, headers = user_agent)
    page_html = response.text
    page_soup = BeautifulSoup(page_html, 'html.parser')
    return page_soup

def scrape_selenium(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() 
    return page_soup

def scrape_firefox(url):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(3)
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() 
    return page_soup

def scrape_selenium_lite(url):
    chrome_options  = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--headless')
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(3)
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() 
    return page_soup

def scrape_selenium_lite2(url):
    chrome_options  = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--headless')
    prefs = {'profile.default_content_setting_values': {'images': 2, #'javascript': 2, 
                            'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(5)
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() 
    return page_soup

def scrape_selenium_netnut(url):
    countries=['sg','in','kr','us']
    country=countries[random.randint(0,len(countries)-1)]
    hostname = "http://gw.ntnt.io"
    port = "5959"
    proxy_username = "shopee-cc-"+country
    proxy_password = "fDCqZWu2"
    chrome_options  = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(hostname + ":" + port))
    chrome_options.add_argument('--disable-notifications')
    # chrome_options.headless = True
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(2)
    pyautogui.typewrite(proxy_username)
    pyautogui.press('tab')
    pyautogui.typewrite(proxy_password)
    pyautogui.press('enter')
    time.sleep(8)
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() 
    return page_soup


def parse_bukalapak_price(page_soup):
    item_price = '-1'
    try:
        try:
            price_container = page_soup.find('div', class_='c-product-price -discounted -main')
            item_price = price_container.text.replace(".", "").replace(",", "").replace("Rp", "")
        except:
            price_container = page_soup.find('div', class_='c-product-price -original -main')
            item_price = price_container.text.replace(".", "").replace(",", "").replace("Rp", "")
    except:
        pass
    return item_price

def parse_lazada_price(page_soup):
    item_price_before = '-1'
    item_price_after = '-1'
    try:
        js = json.loads(page_soup.find('script', type='application/ld+json').text)
        print(js['offers']['lowPrice'])
        try:
            item_price_after = js['offers']['offers'][0]['price']
        # except (TypeError, KeyError):
        #     item_price_after = js['offers']['price']
        except (TypeError, KeyError):
            item_price_after = js['offers']['lowPrice']
        except Exception:
            item_price_after = '-1'
    except:                         
        item_price_after = '-1'
    # Price before discount
    try:
        script = page_soup.find('script', type='text/javascript').text.strip()
        script = script.replace(' ', '').replace('\n', '')
        reg = re.match('.+pdt_price(.+)"(\d+)', str(script))
        item_price_before = reg.group(2)
    except:                         
        item_price_before = '-1'
    return item_price_before, item_price_after

def handling_char(pr, page_soup):
    price = pr
    if '-' in pr:
        st = pr.find('-') 
        try:
            price = int(round(float((pr[:st]))))
        except ValueError as e:
            logging.exception('handling char error 1 ' + str(e) + pr)
            #print('handling char error1 ' + str(pr))
    else:
        try:
            price = int(round(float((pr))))
        except ValueError as e:
            logging.exception('handling char error 2 ' + str(e) + page_soup)
            #print('handling char error2 ' + str(pr))
    return price

# function to parse mobile Toped price
def parse_m_toped_price(page_soup):
    price_m_container = page_soup.findAll("span", {"itemprop": "price"})
    item_m_price = '-1'
    if price_m_container is not None or price_m_container != []:
        item_m_price = handling_char(price_m_container[0].text.replace(".", "").replace(",", ""), page_soup)
    return item_m_price

def parse_toped_price(page_soup):
    try:
        price=page_soup.find('h3',class_='css-c820vl').text.replace('Rp','').replace('.','')
    except:
        price='-1'
    return price

def parse_jdid_price(page_soup):
    original_price='-1'
    final_price='-1'
    # js = json.loads(soup.find("script",type="application/ld+json").text)
    scripts=page_soup.find_all('script', type='text/javascript')
    correct_script=''
    try:
        for script in scripts:
            if 'window.asynData' in script.text:
                correct_script=script.text.replace('\n',' ').replace('\r',' ').strip()
        # print(correct_script)
        json_raw=re.match(".+base: (.+),\s+additional",correct_script).group(1)
        json_file=json.loads(json_raw)
        original_price=json_file['price']['price']
        original_price=str(original_price)
    except:
        pass
    try:
        final_price=page_soup.find('span',class_='sale-price').text
        print(final_price)
        final_price=final_price.replace('Rp','').replace(',','')
    except:
        pass
    return original_price, final_price

def parse_blibli_price(page_soup):
    try:
        price=page_soup.find('span',class_='product__price main-price').span.text.replace('Rp','').replace('.','')
    except:
        price='-1'
    return price

def parse_orami_price(page_soup):
    #if price_container tidak ditemukan
    item_price = "link does not work"
    price_container = (page_soup.find("span", {"class": "final-price"}))
    price_container2 = (page_soup.find("span", {"class": "config-price"}))
    price_container3 = (page_soup.find("div", {"class": "harga-normal final-price"}))
    try:
        item_price = str(price_container['content']).replace('.00','').replace('Rp ','').replace('.','')
    except (AttributeError, KeyError, TypeError):
        try:
            item_price = (price_container2.string).replace('.00','').replace('Rp ','').replace('.','')
        except (AttributeError, KeyError, TypeError): 
            item_price = (price_container3['content']).replace('.00','').replace('Rp ','').replace('.','')
    return item_price

def parse_indomaret_price(page_soup):
    item_price = "link does not work"
    #<span class="normal price-value">Rp 25.900
    price_div = page_soup.find("div", {"class": "price"})
    price_container = price_div.find("span", {"class": "normal price-value"})
    if price_container is not None:
        #item_price = (price_container.text).replace('Rp ','').replace('.','')
        inner_text = [element for element in price_container if isinstance(element, nav)]
        item_price = inner_text[0].replace('Rp ','').replace('.','').replace('\n', '')
    return item_price


def handling_emoji(strx):
    result = "".join(filter(lambda x: x in string.printable, strx))
    return result

def check_link(link):
    if 'http' not in link and (link != "" or link is None or link.lower() == 'not found'):
        link = 'https://' + link
    else:
        link = link
    return link

def get_stats(itemid, shopid):
    oprice = '-1'
    fprice = '-1'
    fe_stock = '-1'
    product_link=''
    try:
        link = 'https://shopee.co.id/api/v2/item/get?itemid=' + str(itemid) + '&shopid=' + str(shopid)
        count = 0
        json_file = json.loads(str(scrape_requests(link)))
        # json_file = json.loads(urllib.request.urlopen(link).read().decode('utf-8'))
        if json_file['item'] is not None:
            oprice = json_file['item']['price_before_discount']/100000
            fprice = json_file['item']['price']/100000
            fe_stock = json_file['item']['stock']
        if oprice == 0 and fprice != 0:
            oprice = fprice
        fprice=int(fprice)
        fprice=str(fprice)
        oprice=int(oprice)
        oprice=str(oprice)
    except:
        pass
    return oprice, fprice, fe_stock


def get_shopee_link(itemid,shopid):
    product_link = 'https://shopee.co.id/product-i.' + str(shopid) + '.' + str(itemid)
    return product_link

def get_shopee_id(shopee_link):
    itemid = ''
    shopid = ''
    try:
        reg_match = re.match('.+shopee.co.id/.+i\.(\d+)\.(\d+)', shopee_link)
        shopid=reg_match.group(1)
        itemid=reg_match.group(2)
    except:
        pass
    return itemid,shopid