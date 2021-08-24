import csv
from bs4 import BeautifulSoup
from selenium import webdriver
#chrome setup
from io import open
import io

import csv
from csv import reader

def get_url(search_term):
    template = "https://www.amazon.co.uk/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(' ', '+')

    url = template.format(search_term)
    #adding pages

    url += '&page={}'
    return url


#item = results[0]
#atag = item.h2.a
#description = atag.text.strip()
#url = 'https://www.amazon.co.uk' + atag.get('href')
#price_parent = item.find('span', 'a-price')
#price_parent.find('span', 'a-price')
#price = price_parent.find('span', 'a-offscreen').text
#rating = item.i.text
#review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text

def numberSearch(url):
    driver.get(url.format(page))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #results = soup.find_all('div', {'data-component-type': 's-search-result'})
    list = soup.find('ul', {"class": "a-pagination"})
    children = list.findChildren('li')
    finalVal = 0
    for child in children:
        #print(child.attrs['class'])
        if child.attrs['class'][0] == 'a-last':
            break
        finalVal = child.text
    return finalVal


def extract_record(item):
    # passing item for a single record and for loop
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.co.uk' + atag.get('href')
    try:
        price_parents = item.find('span', 'a-price')
        price = price_parents.find('span', 'a-offscreen').text
        #price.encode()
        encoded_string = price.encode("ascii", "ignore")
        priceFinal = encoded_string.decode()
    except AttributeError:
        return
    try:

        rating = item.i.text
        rating = rating.split(" ")[0]
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
        review_count = review_count.replace(',', '')
    except AttributeError:
        return
        #rating = ''
        #review_count = ''

    result = (description, priceFinal, rating, review_count, url)
    return result

def numberSearch(url):
    driver = webdriver.Chrome(executable_path="E:/facebook/chromedriver_win32/chromedriver.exe")
    #driver.get(url)
    driver.get(url.format(1))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #results = soup.find_all('div', {'data-component-type': 's-search-result'})
    list = soup.find('ul', {"class": "a-pagination"})
    children = list.findChildren('li')
    finalVal = 0
    for child in children:
        #print(child.attrs['class'])
        if child.attrs['class'][0] == 'a-last':
            break
        finalVal = child.text
    return finalVal


def main(search_term):

    driver = webdriver.Chrome(executable_path="E:/facebook/chromedriver_win32/chromedriver.exe")

    #url = 'https://www.amazon.co.uk/'

    url = get_url(search_term)
    #print(url)
    records = []
    val = numberSearch(url)
    val = int(val)+1
    for page in range(1, val):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()

    with open('new.csv', mode='a', buffering=-1, encoding="utf-8", errors=None, newline=None, closefd=True, opener=None) as f:
        writer = csv.writer(f)
        #writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)


#main('ultrawide monitor')
#with open('new.csv', mode='w', buffering=-1, encoding="utf-8", errors=None, newline=None, closefd=True, opener=None) as f:
#    writer = csv.writer(f)
#    writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
    #writer.writerows(records)

with open('E:/facebook/amazon.csv', mode='r', buffering=-1, encoding="unicode_escape", errors=None, newline=None, closefd=True,
          opener=None) as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object

    for  idx, row in enumerate(csv_reader):
        # row variable is a list that represents a row in csv
        if row[0] != 'ï»¿Health Supplies for Fish & Aquatic Pets' and idx> 168:
            valUsed = row[0].replace('&', '')
            print(valUsed)
            print(idx)
            main(valUsed)