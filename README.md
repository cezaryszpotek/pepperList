# pepperList

A script that creates an ASCI qr code with discounted products of selected stores in form of list.
Project use selenium to scrape website with given parameters.

...

Pepper list generator. Works only in python3

usage: pepperList.py shop_names [-h] [-v] [-t TEMP] [-d DAYS_AGO] [-p PAGES_NUM]

options:
  -h, --help            show this help message and exit
  -v, --visible         disable browser headless mode
  -t TEMP, --temp TEMP  temperature of products on list
  -d DAYS_AGO, --days_ago DAYS_AGO
                        products search from X days ago
  -p PAGES_NUM, --pages_num PAGES_NUM
                        number of pages to search product

...

Example:

$python3 pepperList.py lidl

$python3 pepperList.py auchan lidl neonet -d 9 -t 800 -p 4 -v

...

#REQUIREMENTS

Python pip freeze packages:

attrs==22.1.0
certifi==2022.9.24
charset-normalizer==2.1.1
exceptiongroup==1.0.4
h11==0.14.0
idna==3.4
outcome==1.2.0
packaging==21.3
Pillow==9.3.0
pyparsing==3.0.9
PySocks==1.7.1
python-dotenv==0.21.0
qrcode==7.3.1
requests==2.28.1
selenium==4.6.0
sniffio==1.3.0
sortedcontainers==2.4.0
tqdm==4.64.1
trio==0.22.0
trio-websocket==0.9.2
urllib3==1.26.12
webdriver-manager==3.8.5
wsproto==1.2.0
