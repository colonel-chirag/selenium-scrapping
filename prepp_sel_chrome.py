from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import time
import uploader

from datetime import datetime
from zoneinfo import ZoneInfo

import warnings
import time
import pandas as pd
import logging
# import os
import urllib3


start_time = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
timestamp = start_time.strftime("%Y-%m-%d %H:%M")
pyfilename = 'prepp_sel_chrome'

import sys
# base_path = "/home/notification-scrapers/Prepp_scrapers/"
# base_path = "/root/New_Scrapers/Prepp_scrapers/"
base_path = f"{sys.argv[1]}/Prepp_scrapers/"
print(base_path)
logging.basicConfig(
    filename=f"{base_path}log_files/{pyfilename}.log", 
    level=logging.WARNING)
logger = logging.getLogger()
# handler = RotatingFileHandler(f"{base_path}log_files_backup/{pyfilename}.log", maxBytes=10000,
#                                   backupCount=1)
# logger.addHandler(handler)
logger.warning("Code started")
logger.warning(start_time.strftime("%Y-%m-%d %H:%M:%S"))

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')
chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

PATH = "/usr/bin/chromedriver" #Path to chromedriver (Adjust as needed)

options = {
'proxy': {'http': 'http://brd-customer-hl_a4a3b5b0-zone-competitor_scrapers:llnik27nifws@zproxy.lum-superproxy.io:22225',
'https': 'http://brd-customer-hl_a4a3b5b0-zone-competitor_scrapers:llnik27nifws@zproxy.lum-superproxy.io:22225'},
}
news_articles = []
success = []
failure = []
scrapers_report = []

driver= webdriver.Chrome(PATH, seleniumwire_options=options,options=chrome_options)

official_tag = " prepp official"

#KPSC
try:
    base_url = 'https://kpsc.kar.nic.in/'
    url = 'https://kpsc.kar.nic.in/'
    name = 'KPSC'
    scrapers_report.append([url,base_url,name+official_tag])
    driver.get('https://kpsc.kar.nic.in/')
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    time.sleep(2)
    headlines = soup.find_all('span',attrs={'style':'color:black'})
    for line in headlines:
        headline = line.text
        if headline is not None:
            link = line.find('a')['href'].replace(" ","%20")
            if link.startswith("https"):
                link = link
            else:
                link = url + link
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    name = 'KPSC'
    failure.append((name,e))

driver.quit()

print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)

logger.warning('Successful Scrapers -'+str(success))
logger.warning('Failed Scrapers -'+str(failure))

df = pd.DataFrame(news_articles)
df.drop_duplicates(inplace = True) 
df['date'] = start_time.strftime("%Y-%m-%d %H:%M")
print(df.head())
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
