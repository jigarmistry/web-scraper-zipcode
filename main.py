import csv
import time
import json
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from operator import itemgetter

parser = argparse.ArgumentParser(description='Zipcode and radius')
parser.add_argument('-r', action='store', dest='radius',
                    help='Radius in miles')
parser.add_argument('-z', action='store', dest='zip_code',
                    help='Zipcode')


browser = webdriver.PhantomJS("/usr/local/lib/phantomjs/bin/phantomjs", service_args=[
                              '--ssl-protocol=any', '--ignore-ssl-errors=true', '--load-images=no'])

browser.set_window_size(1600, 900)

url_zipcode = "https://www.freemaptools.com/find-zip-codes-inside-radius.htm"


def get_zipcodes():

    browser.get(url_zipcode)

    radiusElem = browser.find_element_by_id('tb_radius_miles')
    radiusElem.send_keys("24.85")
    zipCodeElem = browser.find_element_by_id('goto')
    zipCodeElem.send_keys("44802")
    drawRadiusBtn = browser.find_element_by_name('Go')
    drawRadiusBtn.click()
    time.sleep(3)

    html_data = browser.find_element_by_id("tb_output").get_attribute('value')
    zip_list = html_data.split(',')
    print zip_list


if __name__ == "__main__":
    results = parser.parse_args()
    print results
    # get_zipcodes()
