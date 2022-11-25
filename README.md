# pepperList

A script that creates a qr code with promotions of selected stores.

Parameters can be used in program:
-d --days - parameter which filter products in range of given days to current day.
-t --temp - parameter which filter products above given number (product points)
-p --pages_num - number of pages that needs to be scrolled down
-h --headless - run browser in background (recommended)

After the given parameter enter the value after equal sign, e.g. --days=5


Example:
$python3 main.py lidl -h
$python3 main.py auchan lidl neonet -d=9 -t=800 -p=4 -h
