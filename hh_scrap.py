import logging
import configparser
import re
import datetime
import urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Reading config file
config = configparser.ConfigParser()
config.read('scrap.cfg')
config_log = config['LOGGING']
region = config['FILTER']['region']
region_area = config['FILTER']['region_area']

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
    jobDict = {}
    titleTag = jobDiv.find("a",{"data-qa":"vacancy-serp__vacancy-title"})
    url = str(titleTag["href"])
    # Skip hhcdn urls
    if re.match('https://hhcdn',url):
        return None
    jobDict["url"] = url
    # Determine if vacancy is in premium placement
    if 'vacancy-serp-item_premium' in jobDiv["class"]:
        jobDict["premium"] = 1
    else:
        jobDict["premium"] = 0
    jobDict["title"] = titleTag.get_text().strip()
    jobDict["company"] = jobDiv.find("a",{"data-qa":"vacancy-serp__vacancy-employer"}).get_text().strip()
    salaryTag = jobDiv.find("div",{"data-qa":"vacancy-serp__vacancy-compensation"})
    if salaryTag == None:
        jobDict["salary"] = 'N/A'
    else:
        jobDict["salary"] = salaryTag.get_text().strip()
    responsibilityTag = jobDiv.find("div",{"data-qa":"vacancy-serp__vacancy_snippet_responsibility"})
    if responsibilityTag == None:
        jobDict["responsibility"] = 'N/A'
    else:
        jobDict["responsibility"] = responsibilityTag.get_text().strip()
    jobRequirement = jobDiv.find("div",{"data-qa":"vacancy-serp__vacancy_snippet_requirement"}).get_text().strip()
    jobIdFilter = re.search('\/(?P<id>\d+)\?*',url)
    jobDict["id"] = jobIdFilter.group('id')
    dateTag = jobDiv.find("span",{"class":"vacancy-serp-item__publication-date"})
    if dateTag == None:
        jobDict["date"] = 'N/A'
    else:
        jobDict["date"] = getJobDate(dateTag.get_text())
    # Send all info to output
    for key,value in jobDict.items():
        print("%s: %s" % (key,value), file=f, flush=True)
    print("", file=f, flush=True)

def getJobDate(jobDate):
    # Get date in dateformat
    today = datetime.date.today()
    todayMonth = today.month
    todayYear = today.year
    monthDict = {'января':'01','февраля':'02','марта':'03','апреля':'04','мая':'05','июня':'06',
    'июля':'07','августа':'08','сентября':'09','октября':'10','ноября':'11','декабря':'12'}
    for month in monthDict.keys():
        if month in jobDate:
            jobDate = jobDate.replace(month,monthDict[month])
            jobMonth = datetime.datetime.strptime(jobDate,'%d %m').month
    # Check if job was published in past year
    if (todayMonth - jobMonth) < 0:
        jobYear = todayYear - 1
    else:
        jobYear = todayYear
    jobDate = datetime.datetime.strptime(jobDate + ' ' + str(jobYear),'%d %m %Y')
    return str(jobDate)

f = open ('jobs.log','w')
baseurl = "https://%s.hh.ru/search/vacancy?specialization=1&area=%s&order_by=publication_time&no_magic=true" % (region,region_area)

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
