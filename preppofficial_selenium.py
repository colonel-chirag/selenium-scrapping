from ast import Name

from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import pandas as pd
#from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import warnings
import time
import sys
# import os
import urllib3
from lxml import etree
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import uploader


start_time = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
timestamp = start_time.strftime("%Y-%m-%d %H:%M")
print (start_time.strftime("%Y-%m-%d %H:%M:%S"))
pyfilename = 'preppofficial_selenium'

import sys
# base_path = "/home/notification-scrapers/Prepp_scrapers/"
# base_path = "/root/New_Scrapers/Prepp_scrapers/"
base_path = f"{sys.argv[1]}/Prepp_scrapers/"
logging.basicConfig(
    filename=f"{base_path}log_files/{pyfilename}.log", 
    level=logging.WARNING)
logger = logging.getLogger()
# handler = RotatingFileHandler(f"{base_path}log_files_backup/{pyfilename}.log", maxBytes=10000,
#                                   backupCount=1)
# logger.addHandler(handler)
logger.warning("Code started")
logger.warning(start_time.strftime("%Y-%m-%d %H:%M:%S"))

options=Options()
options.headless=True
fp=webdriver.FirefoxProfile()
fp.accept_untrusted_certs = True
fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
fp.set_preference("dom.webnotifications.enabled", False)
fp.set_preference("network.cookie.cookieBehavior", 2)

# Driver Initiated
# driver=webdriver.Firefox(options= options)
driver = webdriver.Firefox(options=options,firefox_profile=fp )

news_articles = []
success = []
failure = []
scrapers_report = []
official_tag = " prepp official"

#RPSC
try:
    name = 'RPSC'
    url = 'https://rpsc.rajasthan.gov.in'
    base_url = 'https://rpsc.rajasthan.gov.in'
    scrapers_report.append([url,base_url,name+official_tag])
    # driver = webdriver.Edge(executable_path = 'D:\\edgedriver\\msedgedriver.exe')
    # driver.maximize_window()
    req = driver.get(url)

    time.sleep(2)
    (driver.find_element(By.XPATH,"//*[@id='carouselModal']/div[2]/div/div[3]/button")).click()
    time.sleep(2)
    (driver.find_element(By.XPATH,"//*[@id='aspnetForm']/div[3]/div[1]/div[2]/div[3]/div/div[3]/a")).click()

    elems = driver.find_elements(By.CLASS_NAME, "NewsAnchor")
    j = 0
    for elem in elems:
        if j <= 15:
            text = elem.text[10:]
            link = elem.get_attribute("href")
            news_articles.append((name,text,link))
            # print(name,text,link)
            j+=1
    success.append(name)
    
except Exception as e:
    failure.append((name, e))
    pass

#UPSSSC
try:
    url = 'http://upsssc.gov.in/Default.aspx'
    base_url = "http://upsssc.gov.in/"
    name = 'UPSSSC'
    scrapers_report.append([url,base_url,name+official_tag])
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="fontSize"]/div/div/div/div/div[2]/div/div/div/h3/a').click()
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    headlines = soup.find_all('li',attrs={'style':'color:#0000ee;'})
    for i in range(len(headlines)):
        headline = headlines[i].find('a')['title']
        xpath = '//*[@id="ContentPlaceHolder1_Alert_Silder"]/ul/li[{}]/a'.format(i+1)
        driver.find_element(By.XPATH,xpath).click()
        driver.switch_to.window(driver.window_handles[1])
        link = driver.current_url
        news_articles.append((name,headline,link))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#CGPSC
try:
    url = 'https://www.psc.cg.gov.in/'
    base_url = 'https://www.psc.cg.gov.in/'
    name = 'CG-PSC'
    scrapers_report.append([url,base_url,name+official_tag])
    # driver = webdriver.Edge(executable_path = 'D:\\edgedriver\\msedgedriver.exe')
    # driver.maximize_window()
    req = driver.get(url)
    time.sleep(2)

    # Notification
    Xpath_link = '/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[1]/span/a'
    link_a = driver.find_elements(By.XPATH,Xpath_link)
    for i in range(20):
        # print(link_a[i].text)
        # print(link_a[i].get_attribute('href'))
        text = link_a[i].text
        link = link_a[i].get_attribute('href')
        news_articles.append((name,text,link))
        # print((name,text,link))
    success.append(name)
    
except Exception as e:
    failure.append((name, e))

#WBPSC
try:
    url = 'https://wbpolice.gov.in/WBP/common/WBP_RecruitmentNew.aspx'
    base_url ='https://wbpolice.gov.in'
    name = 'WBPSC'
    scrapers_report.append([url,base_url,name+official_tag])
    driver.get(url)
    for i in range(5):
        driver.find_elements(By.LINK_TEXT,'Get Details')[i].click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        headlines = soup.find('div',attrs={'id':'ctl00_ContentPlaceHolder1_updtR'}).find_all('td',attrs={'align':'left'})
        links = soup.find('div',attrs={'id':'ctl00_ContentPlaceHolder1_updtR'}).find_all('a')
        for i in range(len(headlines)):
            headline = headlines[i].text.strip()
            link = links[i]['href']
            if not link.startswith('https'):
                link = link.replace("../..",'https://wbpolice.gov.in')
            news_articles.append((name,headline,link))
        driver.back()
        time.sleep(2)

    success.append(name)
except Exception as e:
    failure.append((name,e))
    
# RSMSSB(Recruitment Advertisement)

try:
    name = 'RSMSSB(Recruitment Advertisement)'
    base_url = 'https://rsmssb.rajasthan.gov.in/'
    url = 'https://rsmssb.rajasthan.gov.in/page?menuName=EJwE/Y7GD1hMok0YfKTFOtUJMJFGLBa;455611;jbRgWtRe9q4='
    scrapers_report.append([url,base_url,name+official_tag])
    
    driver.get(url)
    for i in range(12):
        try:
            driver.find_element(By.XPATH, f'//*[@id="frmConfignew"]/table/tbody/tr[{i}]/td[3]/a').click()
            rows = driver.find_element(By.ID, 'downLoadId').find_elements(By.TAG_NAME, 'tr')[1:]
            for row in rows:
                headline = row.find_elements(By.TAG_NAME, 'td') [1].text
                link = row.find_elements(By.TAG_NAME, 'td')[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
                print(headline, link)
            driver.back()
            news_articles.append((name, headline, link))
            if name not in success:
                success.append(name)
        except:
            failure.append(('RSMSSB-Recruitment Advertisement', e))
        
except Exception as e:
    failure.append(('RSMSSB-Recruitment Advertisement', e))


driver.quit()
print('Successful Scrapers -', set(success))
print('Failed Scrapers -', set(failure))
df = pd.DataFrame(news_articles)

df['date'] = start_time.strftime("%Y-%m-%d %H:%M")
df.columns = ['source','title','link','date']
# df.drop_duplicates(inplace = True) 

print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)

logger.warning('Successful Scrapers -'+str(success))
logger.warning('Failed Scrapers -'+str(failure))

df = pd.DataFrame(news_articles)
df.drop_duplicates(inplace = True) 
df['date'] = start_time.strftime("%Y-%m-%d %H:%M")
df.columns = ['source','title','link','date']

try:
    uploader.data_uploader(df)
except Exception as e:
    logger.warning("Database Error")
    logger.warning(e)

try:    
    data = pd.read_csv ('/root/New_Scrapers/Cd_scrapers/csv_files/cd_main.csv',on_bad_lines='skip',engine='python')
    data = pd.concat([ data,df])

    data.drop_duplicates(subset = ['title'], inplace = True)
    data.to_csv('/root/New_Scrapers/Cd_scrapers/csv_files/cd_main.csv', index = False)
except Exception as e:
    logger.warning(e)
    logger.warning("error reading or saving the file")

report_df = pd.DataFrame(scrapers_report,columns = ['url','base_url','name'])
report_df['name_of_the_scraper'] = pyfilename

try :

    main_scrapers_report =pd.read_csv(f'{base_path}report/prepp_scrapers_report.csv')
except :
    main_scrapers_report = pd.DataFrame(columns = ['url','base_url','name','name_of_the_scraper'])   

main_scrapers_report= pd.concat([main_scrapers_report,report_df])
main_scrapers_report.drop_duplicates(inplace=True)
main_scrapers_report.to_csv(f'{base_path}report/prepp_scrapers_report.csv',index=False)

#the number of scraper that are scraped
news_count_df = df.groupby('source')['title'].count().reset_index()
news_count_df.columns = ['name'	,'title']
count_report = report_df.merge(news_count_df,
                               on='name',
                               how='left')[['name','title','url']]
count_report.fillna(0,inplace=True)
count_report['date'] = start_time.strftime("%Y-%m-%d %H:%M")
try :
    main_count_report = pd.read_csv(f'{base_path}report/main_count_report.csv')
except :
    main_count_report = pd.DataFrame(columns = ['name','title','url','date'])

main_count_report = pd.concat([count_report , main_count_report])
main_count_report.to_csv(f'{base_path}report/main_count_report.csv',index=False)

logger.warning("Code Ended")
now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
logger.warning(now.strftime("%Y-%m-%d %H:%M:%S"))

print("all done")
