from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup
import requests

# function to grab index prices from yahoo finance using beautiful soup
def getYahooIndexPrice(ticker,spanID):
	r=requests.get("http://finance.yahoo.com/q?s="+ticker)
	data=r.text
	soup=BeautifulSoup(data,"lxml")
	price = soup.find('span', {'id': 'yfs_l10_'+spanID}).text.replace(',', '')
	return price

# function that works out if the market is open and stores the data if it is
# https://en.wikipedia.org/wiki/List_of_stock_exchange_opening_times
# delays: http://finance.yahoo.com/exchanges
def marketIsOpen(ticker):
	# shanghai 
	# 09:15 to 15:00 PLUS Yahoo! 30 minute delay
	if '000001' in ticker:
		now=datetime.now(timezone('Asia/Shanghai'))
		open=now.replace(hour=9,minute=45)
		close=now.replace(hour=15,minute=30)
		if (now > open and now < close and now.isoweekday()):
			return True
		else:
			return False
	
	# new york 
	# 09:30 to 16:00 EST with zero delay
	elif 'GSPC' in ticker:
		now=datetime.now(timezone('America/New_York'))
		open=now.replace(hour=9,minute=30)
		close=now.replace(hour=16,minute=00)
		if (now > open and now < close and now.isoweekday()):
			return True
		else:
			return False

	# london
	# 08:30 to 16:30 PLUS Yahoo 15 minute delay
	elif 'FTSE' in ticker:
		now=datetime.now(timezone('GB'))
		open=now.replace(hour=8,minute=15)
		close=now.replace(hour=16,minute=45)
		if (now > open and now < close and now.isoweekday()):
			return True
		else:
			return False

	# frankfurt
	# 09:00 to 17:45 PLUS Yahoo 15 minute delay
	elif 'DAXI' in ticker:
		now=datetime.now(timezone('CET'))
		open=now.replace(hour=9,minute=15)
		close=now.replace(hour=18,minute=00)
		if (now > open and now < close and now.isoweekday()):
			return True
		else:
			return False

	# tokyo
	# 09:00 to 15:00 PLUS yahoo 30 minute delay
	elif '225' in ticker:
		now=datetime.now(timezone('Asia/Tokyo'))
		open=now.replace(hour=9,minute=30)
		close=now.replace(hour=15,minute=30)
		if (now > open and now < close and now.isoweekday()):
			return True
		else:
			return False

	else:
		print "Ticker "+ ticker+ " not recognized"
		return False

# function to get the local time for an index to store in the database
def getLocalTime(ticker):
	# shanghai 
	if '000001' in ticker:
		return datetime.now(timezone('Asia/Shanghai'))
	
	# new york 
	elif 'GSPC' in ticker:
		return datetime.now(timezone('America/New_York'))

	# london
	elif 'FTSE' in ticker:
		return datetime.now(timezone('GB'))

	# frankfurt
	elif 'DAXI' in ticker:
		return datetime.now(timezone('CET'))

	# tokyo
	elif '225' in ticker:
		return datetime.now(timezone('Asia/Tokyo'))

	else:
		print "Ticker "+ ticker+ " not recognized"
		return False

# function that returns a nicer text representation of the index
def getCleanTicker(ticker):
	# shanghai 
	if '000001' in ticker:
		return "SSE"
	
	# new york 
	elif 'GSPC' in ticker:
		return "S&P500"

	# london
	elif 'FTSE' in ticker:
		return "FTSE100"

	# frankfurt
	elif 'DAXI' in ticker:
		return "DAX"

	# tokyo
	elif '225' in ticker:
		return "N225"

	else:
		print "Ticker "+ ticker+ " not recognized"
		return False

