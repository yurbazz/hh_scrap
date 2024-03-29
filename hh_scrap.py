#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import logging
import configparser
import re
import datetime
import urllib.error
import urllib.request
import sys
import getopt
import dbconn
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar


def get_http_object(url):
    logging.debug("Get url: \n%s", url)
    req = urllib.request.Request(url, None, {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'identity', 'Connection': 'keep-alive'})
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    try:
        response = opener.open(req)
        html = response.read()
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        logging.error(e)
        print("%s \nParser halted, url error..." % e)
        exit()
    else:
        logging.debug("Http received")
        return html


def get_tags_by_attr(bs_obj, tag, fetch_attr):
    logging.debug("Fetch tags <%s> with attr %s" % (tag, fetch_attr))
    tags_list = bs_obj.findAll(tag, fetch_attr)
    if not tags_list:
        logging.error("Elements no found...")
        exit()
    else:
        return tags_list


def get_job_info(job_div):
    job_dict = {}
    title_tag = job_div.find("a", {"data-qa": "vacancy-serp__vacancy-title"})
    url = str(title_tag["href"])
    # Skip hhcdn urls
    if re.match('https://hhcdn', url):
        return None
    job_dict["url"] = url
    # Determine if vacancy is in premium placement
    if 'vacancy-serp-item_premium' in job_div["class"]:
        job_dict["promo"] = 1
    else:
        job_dict["promo"] = 0
    job_dict["title"] = title_tag.get_text().strip()
    company_tag = job_div.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
    if company_tag is None:
        logging.error("Job doesn't have employer, url: %s" % url)
        return None
    else:
        job_dict["company"] = company_tag.get_text().strip()
    salary_tag = job_div.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
    if salary_tag is None:
        job_dict["salary"] = None
    else:
        job_dict["salary"] = salary_tag.get_text().strip()
    responsibility_tag = job_div.find("div", {"data-qa": "vacancy-serp__vacancy_snippet_responsibility"})
    if responsibility_tag is None:
        job_dict["responsibility"] = None
    else:
        job_dict["responsibility"] = responsibility_tag.get_text().strip()
    requirement_tag = job_div.find("div", {"data-qa": "vacancy-serp__vacancy_snippet_requirement"})
    if requirement_tag is None:
        job_dict["requirement"] = None
    else:
        job_dict["requirement"] = requirement_tag.get_text().strip()
    job_id_filter = re.search('/(?P<id>\d+)\?*', url)
    job_dict["id"] = job_id_filter.group('id')
    date_tag = job_div.find("span", {"data-qa": "vacancy-serp__vacancy-date"})
    if date_tag is None:
        job_dict["date"] = None
    else:
        # job_dict["date"] = get_job_date(date_tag.get_text())
        job_date = date_tag.get_text()
        job_date = str(datetime.datetime.strptime(job_date, '%d.%m.%Y'))
        job_dict["date"] = job_date
    return job_dict


def get_job_date(job_date):
    # Get date in dateformat, convert from '01 месяц' to 'yyyy-mm-dd 00:00:00'
    today = datetime.date.today()
    today_month = today.month
    today_year = today.year
    job_year = None
    month_dict = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                  'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11',
                  'декабря': '12'}
    for month in month_dict.keys():
        if month in job_date:
            job_date = job_date.replace(month, month_dict[month])
            job_month = datetime.datetime.strptime(job_date, '%d %m').month
            # Check if job was published in past year
            if (today_month - job_month) < 0:
                job_year = today_year - 1
            else:
                job_year = today_year
    job_date = datetime.datetime.strptime(job_date + ' ' + str(job_year), '%d %m %Y')
    return str(job_date)


def write_to_file(job_info):
    # Send new jobs to file
    with open('jobs.log', 'a') as f:
        for key, value in job_info.items():
            print("%s: %s" % (key, value), file=f, flush=True)
        print("", file=f, flush=True)


def get_job_desc(url):
    # Получаем описание вакансии
    job_id_filter = re.search('/(?P<id>\d+)\?*', url)
    job_id = job_id_filter.group('id')
    html = get_http_object(url)
    bs_obj = BeautifulSoup(html, "lxml")
    div = bs_obj.find("div", {"class": "vacancy-description"})
    if not div:
        logging.error("Job description not found...")
        exit()
    div_filtered = div(["p", "ul"])
    desc = ''
    for element in div_filtered:
        desc += str(element)
    # Вставляем в БД
    dbconn.insert_job_desc(desc, job_id)


def main():
    baseurl = baseurl = "https://%s.hh.ru/search/vacancy?area=%s&clusters=true&enable_snippets=true&industry=7&ored_clusters=true&order_by=publication_time&hhtmFrom=vacancy_search_list&items_on_page=20" % \
              (region, region_area)

    logging.info("=== STARTING SCRAPER ===")
    # Get Pages 1 to 10
    for n in range(0, 10):
        if n == 0:
            url = baseurl
        else:
            url = baseurl + "&page=" + str(n)
        # Вытащим страницу
        html = get_http_object(url)
        # Подготовим страницу для парсинга
        bs_obj = BeautifulSoup(html, "lxml")
        # Вытащим блоки с вакансиями и сохраним в список
        tag = "div"
        fetch_attr = {"class": "vacancy-serp-item"}
        job_list = get_tags_by_attr(bs_obj, tag, fetch_attr)

        logging.info("Get vacancies on Page %s" % (str(n+1)))
        # Получим краткую инфо о вакансии
        for job_div in job_list:
            job_info = get_job_info(job_div)
            if job_info is None:
                continue
            dbconn.job_handler(job_info)
            # if dbconn.job_handler(job_info) == 1:
            #     write_to_file(job_info)


if __name__ == '__main__':
    # Reading config file
    config = configparser.ConfigParser()
    log_date = datetime.date.today()
    log_date = log_date.strftime('%Y-%m-%d')
    if not config.read('scrap.cfg'):
        # If reading from php folder
        config.read('../scrap.cfg')
    config_log = config['LOGGING']
    region = config['FILTER']['region']
    region_area = config['FILTER']['region_area']
    log_filename = config_log['logfile'] + '_' + log_date + '.log'
    if not config.read('scrap.cfg'):
        # If reading from php folder
        log_filename = '../' + log_filename

    # Setup logging
    log_fmt = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(level=config_log['loglvl'], filename=log_filename, format=log_fmt)

    if len(sys.argv) == 1:
        main()
    else:
        opts = []
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'd:')
        except getopt.GetoptError:
            print("Usage: hh_scrap -d <url>")
            exit()
        for opt, arg in opts:
            if opt == '-d':
                get_job_desc(arg)
