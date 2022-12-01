from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium import common
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import argparse
import time
import shelve
import sys
import io
import qrcode
import qrcode.image.svg
import datetime


def seleniumOptions(headless_param):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--enable-javascript')

    if headless_param == 'True':
        options.add_argument('--headless')

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def siteClickDelay(driver, xpth):  # exception catcher when clicking
    break_flag = False
    try:
        wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpth))).click()
    except common.exceptions.StaleElementReferenceException as StaleExcept:
        pass
        try:
            driver.find_element(By.XPATH, xpth).click()
        except common.exceptions.NoSuchElementException:
            break_flag = True
            pass
    except common.exceptions.TimeoutException:
        pass
    except common.exceptions.ElementClickInterceptedException:
        pass

    return break_flag


def findUrl(shoplist, headless_param):  # finding url in foler/site
    db = shelve.open('url_list')

    shopdict = dict()
    notFound = []

    for shopname in shoplist:
        if shopname in db:
            shopdict[shopname] = db[shopname]
            print("%s link found: %s" % (shopname, shopdict[shopname]))
        else:
            print('Searching for %s link' % shopname)
            notFound.append(shopname)

    if len(notFound) != 0:
        driver = seleniumOptions(headless_param)
        driver.get('https://pepper.pl')
        siteClickDelay(driver,
                       '/html/body/div[1]/div[2]/div/section/div/div/div/div/div/div[2]/div[2]/button[1]')  # allow cookies

        for unknownUrl in notFound:
            link = urlScrap(driver, unknownUrl)
            if link != None:
                shopdict[unknownUrl] = link
                db[unknownUrl] = link
                print(link)

        driver.close()
    db.close()

    return shopdict


def urlScrap(driver, shopname):  # scrapping url from site
    textbox = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/header/div/div/div[2]/form/div/span/input')
    textbox.send_keys(Keys.CONTROL + 'a')
    textbox.send_keys(Keys.DELETE)
    textbox.send_keys(shopname)
    textbox.send_keys(Keys.ENTER)

    names = driver.find_elements(By.CLASS_NAME, 'text--color-greyShade.size--all-s')

    namedict = dict()
    for name in names:
        try:
            name_element = name.find_element(By.CLASS_NAME, 'cept-merchant-name')
            link = name.get_attribute('href')
            namedict[name_element.text.lower()] = link
        except common.exceptions.NoSuchElementException:
            pass

    if shopname in namedict:
        return namedict[shopname]
    else:
        if namedict != {}:
            print(shopname, 'not found. Are you looking for:')
            for key in namedict:
                print('-%s' % key)
            ipt = input()

            try:
                return namedict[ipt]
            except KeyError:
                print('Please specify shop name')
        else:
            print(shopname, ' not found')


def searchingCore(name, url, parameters):  # products search

    driver = seleniumOptions(parameters.visible)

    print('\n%s products list from %s days ago:' % (name.title(), parameters.days_ago))

    try:
        driver.get(url)
    except:
        print('Cannot get access to ', url)

    siteClickDelay(driver,
                   '/html/body/div[1]/div[2]/div/section/div/div/div/div/div/div[2]/div[2]/button[1]/span')  # allow cookies else pass
    siteClickDelay(driver, '//*[@id="tour-expired"]/span[2]/span[2]')  # filter bar click
    siteClickDelay(driver, '/html/body/section/div/ul/li[1]/form/ul/li[1]/label/span/span')  # outdated filter

    for i in range(parameters.pages_num):  # rewind more pages
        flag = siteClickDelay(driver, '//*[@id="merchant-deals"]/button')
        if flag:
            break

    time.sleep(1)  # waiting to load all items

    try:  # try to get items
        items = driver.find_elements(By.CLASS_NAME, "threadGrid.thread-clickRoot")

        item_dict = dict()

        for item in items:  # iterate over items
            name = item.find_element(By.CLASS_NAME, 'cept-tt').text  # product name
            if parameters.days_ago != None:
                date = item.find_element(By.CLASS_NAME, 'hide--toW3').text  # product add-date

            try:
                points_given = int(item.find_element(By.CLASS_NAME, "cept-vote-temp").text[:-1])  # product points
            except common.exceptions.NoSuchElementException:
                points_given = 0
            except:
                points_given = 0

            try:
                price = item.find_element(By.CLASS_NAME, 'thread-price').text  # product price
            except common.exceptions.NoSuchElementException:
                price = 'unknown'

            if points_given > int(parameters.temp):
                item_dict[points_given] = name + ': ' + price  # add to list
    except:
        print('Cannot get access to items')

    driver.close()

    txt = ''
    for key in sorted(item_dict, reverse=True):  # print
        txt += str(key) + ": " + str(item_dict[key]) + '\n'
        txt += '\n'

    return txt


def dateCheck(givendate, days_ago):  # hardcoded product`s date check
    givendate = givendate.lower()

    if givendate.startswith('dzisiaj') or givendate.startswith('obowiązuje do') or givendate[0].isdigit():
        return True
    elif givendate.startswith('rozpoczyna') or givendate.startswith('obowiązuje od'):
        return False
    else:
        day = int(''.join([x for x in givendate if x.isdigit()]))
        month = ['sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz', 'paź', 'lis', 'gru'].index(
            ''.join([x for x in givendate if x.isalpha()]).strip()) + 1

        tdy = int(datetime.datetime.today().day)
        currentmonth = int(datetime.datetime.today().month)
        if day + days_ago < tdy and currentmonth == month:
            return False
        else:
            return True


def makeASCIQr(data):  # making qr code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    if data != '':
        qr.add_data(data)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        print(f.read())
        qr.clear()
    else:
        print('Items not found!')


def argPass(shoplist):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Pepper list generator. Work only in python3',
        usage='''pepperList.py shop_names [-h] [-v] [-t TEMP] [-d DAYS_AGO] [-p PAGES_NUM]''')
    parser.add_argument(
        '-v', '--visible', action='store_true',
        default='True', help='disable browser headless mode')
    parser.add_argument(
        '-t', '--temp', type=int,
        default=500, help='temperature of products on list')
    parser.add_argument(
        '-d', '--days_ago', type=int,
        default=7, help='products search from X days ago')
    parser.add_argument(
        '-p', '--pages_num', type=int,
        default=5, help='number of pages to search product')

    parameters = parser.parse_args()

    shopdict = findUrl(shoplist, parameters.visible)

    for name in shopdict:
        makeASCIQr(searchingCore(name, shopdict[name], parameters))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        shoplist = []

        for arg in sys.argv[1:]:
            if arg.startswith('-') or arg.startswith('--'):
                break
            else:
                shoplist.append(arg.lower())
                sys.argv.remove(arg)

        argPass(shoplist)
    else:
        print("Program available only in script mode.")
