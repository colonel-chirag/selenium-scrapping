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
pyfilename = 'counselling_sel'

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

#CLAT
try:
    name = 'CLAT'
    print(name)
    url = 'https://consortiumofnlus.ac.in/clat-2023/'
    base_url = 'https://consortiumofnlus.ac.in'
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    notifications = soup.find_all(class_='notification_link')
    for notification in notifications:
        headline = notification.text.strip()
        a_tag = notification.find('a')
        link = a_tag['href']
        if 'http' not in link:
            link = base_url + link
        news_articles.append((name,headline,link))
    important_events = soup.find_all(class_='notification')
    for event in important_events:
        headline = event.find(class_='notification_msg').text.strip()
        date = event.find(class_='notification_date').text.strip()
        news_articles.append((name,headline,date))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#AILET
try:
    name = 'AILET'
    print(name)
    url = 'https://nationallawuniversitydelhi.in/'
    base_url = 'https://nationallawuniversitydelhi.in'
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    notifications = soup.find_all(class_='notification-row')
    for notification in notifications:
        headline = notification.find(class_='notification-title').text.strip()
        if notification.name == 'a':
            link = notification['href']
        else:
            link = ''
        if 'http' not in link and link != '':
            link = base_url + link
        news_articles.append((name,headline,link))
    important_events = soup.find_all(class_='event-row')
    for event in important_events:
        headline = event.find(class_='event-title').text.strip()
        date = event.find(class_='event-date').text.strip()
        news_articles.append((name,headline,date))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#UPTAC
try:
    name = 'UPTAC'
    print(name)
    url = 'https://uptac.admissions.nic.in/'
    base_url = url
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    news_events = soup.find_all(class_='vc_tta-panel-body')[0].find_all('a')
    for news in news_events:
        headline = news.text.strip()
        link = news['href']
        if 'http' not in link:
            link = base_url + link
        news_articles.append((name,headline,link))
    public_notices = soup.find_all(class_='vc_tta-panel-body')[1].find('ul').find_all('a')
    for notice in public_notices:
        headline = notice.text.strip()
        link = notice['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#TNEA
try:
    name = 'TNEA'
    print(name)
    url = 'https://www.tneaonline.org/'
    base_url = url
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    headlines = soup.find_all(class_='tnea-link-container')
    for line in headlines:
        headline = line.text.strip()
        a_tag = line.find('a')
        if a_tag:
            link = a_tag['href']
            if 'http' not in link:
                link = base_url + link
        else:
            link = ''
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# UP NEET
try:
    name = 'UP NEET'
    print(name)
    url = 'https://upneet.gov.in/'
    base_url = url
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    headlines = soup.find_all(class_='panel-body')[1].find_all('li')
    for line in headlines:
        headline = line.text.strip()
        a_tag = line.find('a')
        if a_tag:
            link = a_tag['href']
            if 'http' not in link:
                link = base_url + link
        else:
            link = ''
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#SAM Odisha
try:
    name = 'SAM Odisha'
    print(name)
    url = 'https://samsodisha.gov.in/DegreeNew/DegreeNoticeDtl.aspx'
    base_url = 'https://samsodisha.gov.in'
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    trs = soup.find('tbody').find_all('tr')[1:]
    for tr in trs:
        headline = ''
        tds = tr.find_all('td')
        headline += 'Date: ' + tds[1].text.strip()
        headline += ' Letter No.: ' + tds[2].text.strip()
        headline += ' Subject: ' + tds[3].text.strip()
        link = tr.find('a')['href'][2:]
        if 'http' not in link:
            link = base_url + link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Calcutta University
try:
    print("univcal")
    url = 'https://www.caluniv.ac.in/news/news.html'
    base_url = url
    scrapers_report.append([url,base_url,"Calcutta University"])
    driver.get(url)
    time.sleep(5)
    articles = driver.find_elements(By.TAG_NAME, 'tr')
    for article in articles[1:]:
        headline= article.text
        link = article.find_element(By.TAG_NAME,'a').get_attribute("href")
        if "http" not in link:
            link = base_url + link
        news_articles.append(("Calcutta University",headline,link))
    success.append('Calcutta University')
except Exception as e:
    failure.append(('Calcutta University',e))
    pass

# University of Calcutta
try:
    print("caluniv")
    url='https://www.caluniv.ac.in/'
    base_url = url
    scrapers_report.append([url,base_url,"University of Calcutta"])
    driver.get(url)
    time.sleep(5)
    results = driver.find_element(By.CLASS_NAME,'container-fluid').find_elements(By.TAG_NAME,'li')
    for result in results:
        headline = result.text
        link = result.find_element(By.TAG_NAME,'a').get_attribute('href')
        if "http" not in link:
            link = base_url + link
        news_articles.append(("University of Calcutta",headline,link))
    success.append('University of Calcutta')
except Exception as e:
    failure.append(('University of Calcutta',e))
    pass

# MPSC
try:
    print("MPSC")
    url="https://mpsc.gov.in/announcement_and_circular?m=4"
    base_url =url 
    driver.get(base_url)
    scrapers_report.append([url,base_url,"MPSC"])
    time.sleep(6)
    results = driver.find_element(By.CLASS_NAME,"table.dataTable.no-footer").find_elements(By.TAG_NAME,'tr')
    for result in results[1:]:
        tds = result.find_elements(By.TAG_NAME,'td')
        subject = tds[2].text
        date = tds[1].text
        headline =  subject + " " + date
        link = result.find_element(By.TAG_NAME,'a').get_attribute('href')
        if "http" not in link:
            link = base_url + link
        news_articles.append(("MPSC",headline,link))
    success.append('MPSC')
except Exception as e:
    failure.append(('MPSC',e))
    pass

# IIM Ranchi
try:
    url = "https://www.iimranchi.ac.in/"
    print("IIM Ranchi")
    base_url = url
    name = 'IIM Ranchi'
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(3)
    results = driver.find_elements(By.CLASS_NAME,"col-lg-4")
    for i in results[1:4]:
        li = i.find_elements(By.TAG_NAME, "li")
        for j in li:
            headline = j.text
            link = j.find_element(By.TAG_NAME , "a").get_attribute('href')
            if "http" not in link:
                link = base_url + link
            news_articles.append(("IIM Ranchi",headline,link))
    success.append('IIM Ranchi')
except Exception as e:
    failure.append((name,e))
    pass


# # BHU(21/2)(Redo)
try:
    name = 'BHU'
    print(name)
    base_url = "https://www.bhu.ac.in"
    url1 = "https://www.bhu.ac.in/Site/Notices/1_2_16_Main-Site"
    url_x="https://www.bhu.ac.in/Site/NoticeDetail/1_2_16_Main-Site?"
    scrapers_report.append([url1, base_url, name])
    driver.get(url1)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    resultss = soup.find("ul", class_="events-academ")
    results = resultss.find_all("a", class_="ng-binding")
    for result in results:
        headline = result.text.strip()
        link = url_x + result.get("href").split("(")[-1].split(")")[0]
        news_articles.append(('BHU', headline, link))

    url2 = "https://www.bhu.ac.in/Site/NewsList/1_2_16_Main-Site"
    url_x="https://www.bhu.ac.in/Site/NewsDetail/1_2_16_Main-Site?"
    scrapers_report.append([url2, base_url, name])
    driver.get(url2)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    resultss = soup.find("ul", class_="events-academ")
    results = resultss.find_all("a", class_="ng-binding")
    for result in results:
        headline = result.text.strip()
        link = url_x + result.get("href").split("(")[-1].split(")")[0]
        news_articles.append(('BHU', headline, link))

    url3 = "https://www.bhu.ac.in/Site/EventsList/1_2_16_Main-Site?Upcoming"
    url_x="https://www.bhu.ac.in/Site/EventDetails/1_2_16_Main-Site?Upcoming&"
    scrapers_report.append([url3, base_url, name])
    driver.get(url3)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    resultss = soup.find("ul", class_="events-academ")
    results = resultss.find_all("a", class_="ng-binding")
    for result in results:
        headline = result.text.strip()
        link = url_x + result.get("href").split("(")[-1].split(")")[0]
        news_articles.append(('BHU', headline, link))
    success.append('BHU')
except Exception as e:
    failure.append(('BHU', e))
    pass
# end_time = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
# timestamp = end_time.strftime("%Y-%m-%d %H:%M")
# print(timestamp)
# IIT BHU(21/2)
try:
    name = "IIT Bhu"
    print(name)
    base_url = 'https://www.iitbhu.ac.in'
    url = "https://www.iitbhu.ac.in/alerts"
    scrapers_report.append([url, base_url, name])
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = soup.find('div', class_="node__content clearfix").find_all('a')
    for result in results:
        headline = result.text.strip()
        link = result.get("href")
        if 'http' not in link:
            link = base_url + link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

#AIMS Patna(21/2)
try:
    name='AIIMS Patna'
    print(name)
    url='https://aiimspatna.edu.in/'
    base_url=url
    scrapers_report.append([url, base_url, name])
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    div=soup.find('div',class_="about-content important").find('marquee')
    tags= div.find_all('a')
    for a in tags:
        headline=a.text
        link=a.get("href")
        if 'http' not in link:
            link = base_url + link
        news_articles.append((name, headline, link))
    success.append('AIMS Patna')
except Exception as e:
    failure.append(('AIMS Patna',e))
    pass

# SU Digital
try:
    name = 'SU Digital'
    print(name)
    url = 'https://su.digitaluniversity.ac/HomeContentDisplay.aspx?Content_Type=1'
    base_url = url
    scrapers_report.append([url,base_url,'SU Digital'])
    driver.get(url)
    time.sleep(5)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find('div',id='mastercontentbox').find_all('li',class_='item')
    for result in results:
        headline = result.text.strip()
        link=result.find('a').get('href')
        if "http" not in link:
            link = base_url+link
        news_articles.append(('SU Digital',headline,link))
    success.append('SU Digital')
except Exception as e:
    failure.append(('SU Digital',e))
    pass

#Christian Medical College
try:
    name = 'Christian Medical College'
    print(name)
    url = 'https://www.cmcludhiana.in/'
    driver.get(url)
    base_url = url
    scrapers_report.append([url, base_url, name])
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.find('div', class_="news-updates")
    ats = div.find_all('a')
    for a in ats:
        text = a.text.strip()
        link = a['href']
        if 'http' not in link:
            link = url + link
        news_articles.append((name, text, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

#NIFT
try:
    name = 'NIFT'
    print(name)
    url = 'https://nift.ac.in/admission'
    base_url = url
    scrapers_report.append([url,base_url,name])
    driver.get(url)
    time.sleep(3)
    #print(content.status_code)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    headlines = soup.find(class_='card-text').find_all('li')
    for line in headlines:
        a_tag = line.find('a')
        headline = line.text.strip()
        if a_tag:
            link = a_tag['href']
            if 'http' not in link:
                link = base_url + link
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))

#SXUK
try:
    url = "https://sxuk.edu.in/admission_notice"
    base_url = "https://sxuk.edu.in"
    name = "SXUK"
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    results = soup.find_all("div", class_= "sub-head-faculty")       
    for i in results:
        link_tag = i.find('a')
        if link_tag:
           link = link_tag["href"]
        headline=i.text.strip()
        if "http" not in link:
                link = base_url + link
        news_articles.append((name , headline , link ))
    success.append(name)
except Exception as e:
    failure.append((name, e))

driver.quit()

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
