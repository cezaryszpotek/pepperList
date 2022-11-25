# pepperList

A script that creates a ASCI qr code with discounted products of selected stores in form of list.
Project use selenium to scrape website with given parameters.


Parameters can be used in program:

-d --days - parameter which filter products in range of given days to current day.

-t --temp - parameter which filter products above given number (product points)

-p --pages_num - number of pages that needs to be scrolled down

-h --headless - run browser in background (recommended)

After the given parameter enter the value after equal sign, e.g. --days=5



Example:

$python3 main.py lidl -h

$python3 main.py auchan lidl neonet -d=9 -t=800 -p=4 -h



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
