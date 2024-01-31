from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service

driver_service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=driver_service)


news_articles=[]
links = []
success=[]
failure=[]
scrapers_report=[]
link=[]

#medicaldialogues
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