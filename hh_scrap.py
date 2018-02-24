import logging
import configparser
import urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Reading config file
config = configparser.ConfigParser()
config.read('scrap.cfg')
config_log = config['LOGGING']
region = config['FILTER']['region']

# Setup logging
log_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=config_log['loglvl'],filename=config_log['logfile'],format=log_fmt)

def getHTTPObject(url):
    logging.debug("Get url: \n%s", url)
    try:
        html = urlopen(url) # return byte object
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        logging.error(e)
        print("%s \nParser halted, url error..." % (e))
        exit()
    else:
        logging.debug("Http recieved")
        return html

def getTagsByAttr(tag,**attr):
    for key in attr:
        logging.debug("Fetch tags <%s> with attr %s=%s" % (tag,key,attr[key]))
        tagsList = bsObj.findAll(tag,{key:attr[key]})
    if tagsList == []:
        logging.error("Elements no found...")
        exit()
    else:
        return tagsList

def getJobInfo(jobDiv):
    jobTitle = jobDiv.find("a",{"data-qa":"vacancy-serp__vacancy-title"})
    jobUrl = str(jobTitle["href"])
    jobTitle = jobTitle.get_text()
    jobCompany = jobDiv.find("a",{"data-qa":"vacancy-serp__vacancy-employer"}).get_text().lstrip()
    jobSalary = jobDiv.find("div",{"data-qa":"vacancy-serp__vacancy-compensation"})
    if jobSalary == None:
        jobSalary = 'N/A'
    else:
        jobSalary = jobSalary.get_text()
    jobDate = jobDiv.find("span",{"class":"vacancy-serp-item__publication-date"})
    if jobDate == None:
        jobDate = 'N/A'
    else:
        jobDate = jobDate.get_text()
    f.write(jobTitle + '\n' + jobUrl + '\n' + jobCompany + '\n' + jobSalary + '\n' +
    jobDate + '\n\n')

f = open ('jobs.log','w')
baseurl = "https://%s.hh.ru/search/vacancy?specialization=1&area=3&order_by=publication_time&no_magic=true" % region

logging.info("=== STARTING SCRAPER ===")
# Get Pages 1 to 2
for n in range(0,2):
    if n == 0:
        url = baseurl + "&text=&currency_code=RUR&experience=doesNotMatter&search_period=&items_on_page=20"
    else:
        url = baseurl + "&enable_snippets=true&clusters=true&page=" + str(n)
    # Вытащим страницу
    html = getHTTPObject(url)
    # Подготовим страницу для парсинга
    bsObj = BeautifulSoup(html,"lxml")
    # Вытащим блоки с вакансиями и сохраним в список
    fetchAttr = {"class":"vacancy-serp-item"}
    jobList = getTagsByAttr("div",**fetchAttr)

    logging.info("Get vacancies on Page %s" % (str(n+1)))
    f.write("Page %s\n\n" % (str(n+1)))
    # Получим краткую инфо о вакансии
    for jobDiv in jobList:
        getJobInfo(jobDiv)

f.close()
logging.info("=== SCRAPER STOPED ===")
