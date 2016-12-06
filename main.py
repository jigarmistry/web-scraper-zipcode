import csv
import time
import argparse
import requests
import openpyxl as px
from selenium import webdriver


parser = argparse.ArgumentParser(description='Zipcode and radius')
parser.add_argument('-r', action='store', dest='radius',
                    help='Radius in miles')
parser.add_argument('-z', action='store', dest='zip_code',
                    help='Zipcode')


browser = webdriver.PhantomJS("/usr/local/lib/phantomjs/bin/phantomjs", service_args=[
                              '--ssl-protocol=any', '--ignore-ssl-errors=true', '--load-images=no'])

browser.set_window_size(1600, 900)

url_zipcode = "https://www.freemaptools.com/find-zip-codes-inside-radius.htm"
url_grades = "http://education.ohio.gov/getattachment/Topics/Data/Report-Card-Resources/DISTRICT-GRADES.xlsx"


def get_zipcodes(miles, zip_code):

    browser.get(url_zipcode)

    radiusElem = browser.find_element_by_id('tb_radius_miles')
    radiusElem.send_keys(miles)
    zipCodeElem = browser.find_element_by_id('goto')
    zipCodeElem.send_keys(zip_code)
    drawRadiusBtn = browser.find_element_by_name('Go')
    drawRadiusBtn.click()
    time.sleep(5)

    html_data = browser.find_element_by_id("tb_output").get_attribute('value')
    zip_list = html_data.split(',')
    return zip_list


def get_district_grades(zip_list):

    download_data = requests.get(url_grades).content
    xls_file = open('district_grades_input.xlsx', 'wb')
    xls_file.write(download_data)
    xls_file.close()

    grades = []
    a = 0
    W = px.load_workbook('district_grades_input.xlsx')
    p = W.get_sheet_by_name(name='DISTRICT')
    header = []
    for row in p.iter_rows():
        in_list = []
        for k in row:
            if a != 0:
                in_list.append(k.internal_value)
            else:
                header.append(k.internal_value)
        if in_list != []:
            grades.append(in_list)
        a = a + 1

    grades.sort(key=lambda row: row[10])

    output_grades = []
    for i in grades:
        zipr = i[5][0:5]
        if zipr != "" and zipr in zip_list:
            output_grades.append(i)

    wb = px.Workbook()
    dest_filename = 'district_grades_output.xlsx'
    ws1 = wb.active
    ws1.title = "district grades"
    ws1.append(header)
    for orow in output_grades:
        ws1.append(orow)
    wb.save(filename=dest_filename)


if __name__ == "__main__":

    options = parser.parse_args()
    if options.radius and options.zip_code:
        zip_list = get_zipcodes(options.radius, options.zip_code)
        if zip_list != []:
            get_district_grades(zip_list)
        else:
            print ("No Zipcodes Founds")
    else:
        print("")
        print("Please provide the zipcode/radius")
        print("")
        parser.print_help()
