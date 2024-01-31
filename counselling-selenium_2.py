from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import time

from datetime import datetime
from zoneinfo import ZoneInfo

import warnings
import time
import pandas as pd
import logging
# import os
import urllib3
import uploader


start_time = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
timestamp = start_time.strftime("%Y-%m-%d %H:%M")
print(timestamp)
pyfilename = 'counselling_sel_2'

import sys
# base_path = "/home/notification-scrapers/Cd_scrapers/"
# base_path = "/root/New_Scrapers/Cd_scrapers/"
base_path = f"{sys.argv[1]}/Cd_scrapers/"
#print(base_path)
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

# cluster university jammu(20/2)
try:
    page = 1
    name = "cu jammu"
    print(name)
    for page in range(1,30):
        base_url = "https://clujammu.ac.in/v1/"
        url = f"https://clujammu.ac.in/v1/notifications.php?id=admission&page={page}"
        driver.get(url)
        time.sleep(2)
        scrapers_report.append([url, base_url, name])
        #driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find('div', class_="tab-lesson active")
        for result in results.find_all('a'):
            headline = result.text.strip()
            link = base_url + result.get("href")
            news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# N. L. Dalmia Institute of Management Studies and Research(20/2)
try:
    name = 'N. L. Dalmia Institute of Management Studies and Research'
    print(name)
    url = 'https://www.nldalmia.in/'
    base_url = url
    driver.get(url)
    time.sleep(2)
    scrapers_report.append([url, base_url, name])
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.find('div', class_="modal-body-pop")
    for a in div.find_all('a'):
        text = a.text
        link = a['href']
        if 'http' not in link:
            link = url + link
        news_articles.append((name, text, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass


#University of Burdwan
try:
    url = "http://www.buruniv.ac.in/"
    base_url = url
    name = 'BRUNIV'
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find_all(class_='container-fluid row-panels')[3].find(class_='col-sm-4').find_all('li')
    for i in results:
        headline = i.text.strip()
        link = i.find('a')['href'].replace('../',base_url)
        if "http" not in link:
            link = base_url + link
        news_articles.append(("BRUNIV",headline,link))
    success.append('BRUNIV')
except Exception as e:
    failure.append((name,e))
    pass
#HNBGU
try:
    url = "https://hnbgu.ac.in"
    base_url = url
    name = 'HNBGU'
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find(class_='arrow_list').find_all('a')
    for i in results:
        headline = i.text.strip()
        link = i['href']
        if "http" not in link:
            link = base_url + link
        news_articles.append(("HNBGU",headline,link))
    success.append('HNBGU')
except Exception as e:
    failure.append((name,e))
    pass

try:
    url = "https://medicaldialogues.in/news/education"
    base_url = "https://medicaldialogues.in/news/education"
    name = "medicaldialogues"
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scrapers_report.append([url,base_url,name])
    articles = soup.find("div", class_="col-sm-8 content-column").find_all('p')
    for i in articles:
        link_tag = i.find('a')
        if link_tag:
            link = link_tag["href"]
            headline=link_tag.text
            if "http" not in link:
                link = base_url + link
            news_articles.append((name , headline , link ))
    success.append(name)
except Exception as e:
    failure.append((name, e))

print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)
logger.warning('Successful Scrapers -'+str(success))
logger.warning('Failed Scrapers -'+str(failure))
now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
df = pd.DataFrame(news_articles)
df.drop_duplicates(inplace = True) 
df['date'] = now.strftime("%Y-%m-%d %H:%M")
df.columns = ['source','title','link','date']


try:
    uploader.data_uploader(df)
except Exception as e:
    logger.warning("Database Error")
    logger.warning(e)

try:    
    data = pd.read_csv ('/root/New_Scrapers/Cd_scrapers/csv_files/cd_main.csv',on_bad_lines='skip',engine='python')
    data = pd.concat([ data,df])

    data.drop_duplicates(subset = 
                         ['title'], inplace = True)
    data.to_csv('/root/New_Scrapers/Cd_scrapers/csv_files/cd_main.csv', index = False)
except Exception as e:
    logger.warning(e)
    logger.warning("error reading or saving the file")

report_df = pd.DataFrame(scrapers_report,columns = ['url','base_url','name'])
report_df['name_of_the_scraper'] = pyfilename

try :

    main_scrapers_report =pd.read_csv(f'{base_path}report/cdmain_scrapers_report.csv')
except :
    main_scrapers_report = pd.DataFrame(columns = 
                                        ['url','base_url','name',
                                         'name_of_the_scraper'])   

main_scrapers_report= pd.concat([main_scrapers_report,report_df])
main_scrapers_report.drop_duplicates(inplace=True)
main_scrapers_report.to_csv(f'{base_path}report/cdmain_scrapers_report.csv',index=False)

#the number of scraper that are scraped
df['domain'] = df['source'].str.split(":").str[-1]
news_count_df = df.groupby('domain')['title'].count().reset_index()
news_count_df.columns = ['name'	,'title']
news_count_df['name'] = news_count_df['name'].str.strip()
count_report = report_df.merge(news_count_df,
                               on='name',
                               how='left')[['name','title','url']]
count_report.fillna(0,inplace=True)
count_report['date'] = now.strftime("%Y-%m-%d %H:%M")
try :
    main_count_report = pd.read_csv(f'{base_path}report/main_count_report.csv')
except :
    main_count_report = pd.DataFrame(columns = ['name','title','url','date'])

main_count_report = pd.concat([count_report , main_count_report])
main_count_report.to_csv(f'{base_path}report/main_count_report.csv',index=False)

logger.warning("Code Ended")
logger.warning(now.strftime("%Y-%m-%d %H:%M:%S"))

print("all done")
