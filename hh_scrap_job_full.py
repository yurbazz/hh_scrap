import logging
import configparser
import urllib.error
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_http_object(url):
    logging.debug("Get url: \n%s", url)
    try:
        html = urlopen(url)  # return byte object
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        logging.error(e)
        print("%s \nParser halted, url error..." % e)
        exit()
    else:
        logging.debug("Http received")
        return html


def main(url):
    html = get_http_object(url)
    bs_obj = BeautifulSoup(html, "lxml")
    div = bs_obj.find("div", {"class": "vacancy-description"})
    div_filtered = div(["p", "ul"])
    desc = ''
    for element in div_filtered:
        desc += str(element)
    print(desc)


if __name__ == '__main__':
    # Reading config file
    config = configparser.ConfigParser()
    config.read('scrap.cfg')
    config_log = config['LOGGING']

    # Setup logging
    log_fmt = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(level=config_log['loglvl'], filename=config_log['logfile'], format=log_fmt)

    try:
        logging.info("Get full job description")
        main(sys.argv[1])
    except IndexError:
        logging.error("Url parameter is empty")
        exit()
