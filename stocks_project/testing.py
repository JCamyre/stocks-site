from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
from GoogleNews import GoogleNews
from dotenv import load_dotenv
import os 
import tweepy 

# Could I simplify a lot of this using pd.read_html(str(soup.find('table')))

pd.options.display.max_columns = 10
# jupyter notebook

# Make sure to install python-dotenv, not pip install dotenv

# Add to Py-Trading, 1.0.0

# With the amount I am accessing finviz, would it be easier to make an API?
# Each stock is an object, use .get_news(), .get_price_targets(), etc.

# Make this a class, then for all of these don't need ticker, just do self.ticker

# Code reuse

def _find_match(pattern, text):
	match = pattern.search(text)
	return match

def _no_attributes(tag):
	if 'td' in str(tag):
		return tag.has_attr('class') or tag.has_attr('id')

def _get_soup(url):
	response = get(url, headers=HEADERS, timeout=20)
	assert response.status_code == 200
	return BeautifulSoup(response.content, 'lxml')


HEADERS = {'User-Agent': "'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) AppleWebKit/537.36 " # Telling the website what browser I am "using"
							 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}

# Make this all one big function
def _get_summary(ticker):
	BASE_URL = f'https://www.marketwatch.com/investing/stock/{ticker}'
	soup = _get_soup(BASE_URL)

	summary = soup.find('p', {'class': 'description__text'})

	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'
	soup = _get_soup(BASE_URL)
	website = soup.find('a', {'title': 'Company Profile'})
	if website:
		website = website['href']

	return summary.get_text(), website


	# Find the website of the stock and go to its information page

def _basic_stats(ticker):
	# Market cap, avg volume, price, chart, 
	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
	soup = _get_soup(BASE_URL)

	with open('output1.html', 'w', encoding='utf-8') as file:
		file.write(str(soup))

	# Financial highlights
	div = soup.find('div', {'class': 'Mb(10px) Pend(20px) smartphone_Pend(0px)'})
	print([(i.find('h3', {'class': 'Mt(20px)'}), i.find('tbody').find_all('tr')) for i in div.find_all('div', {'class': 'Pos(r) Mt(10px)'})])

	# Trading Information
	div = soup.find('div', {'class': 'Pstart(20px) smartphone_Pstart(0px)'})
	print([(i.find('h3', {'class': 'Mt(20px)'}), i.find('tbody').find_all('tr')) for i in div.find_all('div', {'class': 'Pos(r) Mt(10px)'})])

	# Income Statement
	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
	soup = _get_soup(BASE_URL)

	# Balance Sheet
	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
	soup = _get_soup(BASE_URL)
	pass

def _price_target(ticker, exchange='NASDAQ'): # To do: Automatically find correct stock exchange
	BASE_URL = f'https://www.marketbeat.com/stocks/{exchange}/{ticker}/price-target/'
	soup = _get_soup(BASE_URL)
	table = soup.find('table', {'class': "scroll-table"})
	# price_target = soup.find('table', {'class': 'scroll-table'})
	_pattern = re.compile(r'Price Target: \$\d{1,3}\.\d\d')
	price_target = _find_match(_pattern, table.get_text()).group(0)
	_pattern = re.compile(r'\d{1,3}\.\d\d\% \w{6,8}')
	percentage = _find_match(_pattern, table.get_text()).group(0)

	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	response = get(BASE_URL, headers=HEADERS, timeout=20)
	soup = BeautifulSoup(response.content, 'lxml')
	table = soup.find('table', {'class': "fullview-ratings-outer"})
	rows = table.find_all('td', {'class': 'fullview-ratings-inner'})
	df_data = []
	for row in rows:
		row = row.find_all('td')
		date, _, fund, action, pricetarget = [val.get_text() for val in row]
		date = datetime.strptime(date, '%b-%d-%y')
		df_data.append((date, fund, action, pricetarget))

	analyst_price_targets = pd.DataFrame(df_data, columns=['Date', 'Fund', 'Action', 'PriceTarget'])
	analyst_price_targets = analyst_price_targets.set_index('Date')
	return price_target, percentage, analyst_price_targets


# html = soup.prettify("utf-8") Good way to visualize what your Python code is visualizing
# with open('output1.html', 'w', encoding='utf-8') as f:
# 	f.write(str(_price_target('AAPL')))

def _price_predictions(ticker):
	BASE_URL = f'https://www.barchart.com/stocks/quotes/{ticker}/opinion'
	soup = _get_soup(BASE_URL)

	table = soup.find('table', {'data-ng-class': "{'hide': currentView !== 'strengthDirection'}"})
	titles = soup.find_all('tr', {'class': 'indicator-title'})
	titles = [i.get_text() for i in titles]

	data = soup.find_all('tr', {'class': 'indicator-item'})
	data = [i.get_text() for i in data]
	data = data[len(data)//2 + 1:]
	df_data = []
	for i in data:
		signal, strength, direction = i.split()[-3:]
		indictator = ' '.join(i.split()[:-3])
		df_data.append((indictator, signal, strength, direction))
	df = pd.DataFrame(df_data, columns=['Indictator', 'Signal', 'Strength', 'Direction'])
	print(df.head())

def _ta_indictators(ticker, exchange='NASDAQ'): # Loads wrong page. Beta, RSI history, above/below 9 SMA, above/below 180 SMA, volatility, rel volume
	BASE_URL = f'https://www.tradingview.com/symbols/{ticker}/technicals/'
	# Modify _get_soup function for special purpose (acquisition company).
	response = get(BASE_URL, headers=HEADERS, timeout=20)
	assert response.status_code == 200
	exchange = response.url.split('/')[-2]

	BASE_URL = f'https://www.tradingview.com/symbols/{exchange}/technicals/'
	print(BASE_URL)
	soup = _get_soup(BASE_URL)

	print(soup.get_text())


	with open('output1.html', 'w', encoding='utf-8') as file:
		file.write(str(soup))

	# print(soup.find('a', {'href': "/scripts/relativestrengthindex/"}))

	# Buy or sell (Summary, Oscillators, Moving Averages)
	s = soup.find_all('div', {'class': 'speedometerWrapper-1SNrYKXY'})

	# Oscillators
	oscillators = soup.find('div', {'class': 'container-2w8ThMcC tableWithAction-2OCRQQ8y'})

_ta_indictators('CCIV')

def _news_sentiments(ticker): # Returns news articles curated via Finviz, Yahoo, and Google News, GET UNUSUAL OPTION ACTIVITY
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)

	table = soup.find('table', {'class': 'fullview-news-outer'})
	rows = table.find_all('tr')
	df_data = []
	for row in rows:
		date = row.find('td', {'align': 'right'})
		article = row.find('td', {'align': 'left'})
		link = article.find('a')['href']
		df_data.append((date.get_text(), article.get_text(), link))
	df = pd.DataFrame(df_data, columns=['Time', 'Headline', 'Link'])

	# Getting news from google news search
	googlenews = GoogleNews(lang='en', period='14d') # Specify period for news
	googlenews.search(ticker) 
	# print([(i, j) for i, j in zip(googlenews.get_texts(), googlenews.get_links())])
	# To get other pages, do googlenews.get_page(2), etc.

	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/news?p={ticker}'
	soup = _get_soup(BASE_URL)

	links = soup.find_all('a', {'class': 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'})
	print([(link.get_text(), str('yahoo.com' + link['href'])) for link in links])

	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/press-releases?p={ticker}'
	soup = _get_soup(BASE_URL)

	links = soup.find_all('a', {'class': 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'})
	print([(link.get_text(), str('yahoo.com' + link['href'])) for link in links])
	# Look for keywords in the news? Any showcases, Investor/analyst days, Analyst revisions, Management transitions
	# Product launches, Significant stock buyback changes

	return df

def _financials(ticker): # OMEGALUL
	# Displaying all information. Could leave this as a dictionary.
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)
	table = soup.find('table', {'class': 'snapshot-table2'})
	labels = table.find_all('td', {'class': 'snapshot-td2-cp'})
	values = table.find_all('td', {'class': 'snapshot-td2'})
	info_dict = {}
	for label, val in zip(labels, values):
		info_dict[str(label.get_text())] = str(val.get_text()) 
	df = pd.DataFrame(info_dict.items(), columns={'Label', 'Value'})

	# yo
	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
	soup = _get_soup(BASE_URL)

	# PE/G, market cap, profit margin, idk what else is important
	div = soup.find('div', {'id': 'quote-summary'})
	return df, 'Avg. Volume: ' + div.find('span', {'data-reactid': '48'}).get_text(), 'Market Cap: ' + div.find('span', {'data-reactid': '56'}).get_text(), 
	'Beta (5Y Monthly): ' + div.find('span', {'data-reactid': '61'}).get_text(), 'PE Ratio (TTM): ' + div.find('span', {'data-reactid': '66'}).get_text()

def _short_selling(ticker):
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)

	labels = soup.find_all('td', {'class': 'snapshot-td2-cp'})
	values = soup.find_all('td', {'class': 'snapshot-td2'})
	return labels[16].get_text(), values[16].get_text(), labels[22].get_text(), values[22].get_text()


def _put_call_ratio(ticker): 
	BASE_URL = f'https://www.alphaquery.com/stock/{ticker}/volatility-option-statistics/120-day/put-call-ratio-oi'
	soup = _get_soup(BASE_URL)

	ratio_volume = soup.find('tr', {'id': 'indicator-put-call-ratio-volume'})
	ratio_open_interest = soup.find('tr', {'id': 'indicator-put-call-ratio-oi'})
	forward_price = soup.find('tr', {'id': 'indicator-forward-price'})
	call_breakeven_price = soup.find('tr', {'id': 'indicator-call-breakeven'})
	put_breakeven_price = soup.find('tr', {'id': 'indicator-put-breakeven'})
	option_breakeven_price = soup.find('tr', {'id': 'indicator-option-breakeven'})

	return ratio_volume, ratio_open_interest, forward_price, call_breakeven_price, put_breakeven_price, option_breakeven_price

def _find_competition(ticker):
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)

	td = soup.find_all('td', {'class': 'fullview-links'})[1]
	sectors = td.find_all('a', {'class': 'tab-link'})
	sector_urls = ([str('https://finviz.com/' + i['href']) for i in sectors])
	for i in sector_urls: # Find stocks with similar P/E ratios and market cap, then track difference in performance
		print(i)
		print('')

def _etfs(ticker):
	BASE_URL = f'https://etfdb.com/stock/{ticker}/'
	soup = _get_soup(BASE_URL)
	tbody = soup.find('tbody')
	rows = tbody.find_all('tr')
	rows = [[i.get_text() for i in row.find_all('td')] for row in rows]
	train_df = pd.DataFrame(rows, columns={'Ticker', 'ETF', 'ETF Category', 'Expense Ratio', 'Weighting'})
	return train_df

def _insider_trading(ticker):
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)

	tr = soup.find_all('tr', {'class': "insider-sale-row-2"})
	return [i.get_text() for i in tr]

def _social_media_sentiment(ticker, num_of_tweets=50): # Also reddit sentiment, and twitter
	# Twitter
	load_dotenv()
	consumer_key = os.getenv('API_KEY')
	consumer_secret = os.getenv('API_SECRET_KEY')
	auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True)
	tweets = []
	for i, tweet in enumerate(tweepy.Cursor(api.search, q=f'${ticker}', count=num_of_tweets).items(num_of_tweets)):
		tweets.append((i, tweet.text, tweet.author.screen_name, tweet.retweet_count, tweet.favorite_count, tweet.created_at))
	return tweets

def _catalysts(ticker): # Returns date of showcases, FDA approvals, earnings, etc
	# Earnings date: 
	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
	soup = _get_soup(BASE_URL)

	earnings_date = soup.find('td', {'data-test': 'EARNINGS_DATE-value'})
	print(f'Next earnings date: {earnings_date.get_text()}')

	# FDA approvals
	BASE_URL = 'https://www.rttnews.com/corpinfo/fdacalendar.aspx'
	soup = _get_soup(BASE_URL)

	df_data = []
	company = soup.find_all('div', {'data-th': 'Company Name'})
	print(company[0].get_text())

	events = soup.find_all('div', {'data-th': 'Event'})
	print(events[0].get_text())

	outcome = soup.find_all('div', {'data-th': 'Outcome'})
	if outcome[0]:
		print(outcome[0].get_text())

	dates = soup.find_all('span', {'class': 'evntDate'})
	print([date.get_text() for date in dates])

	for i in range(len(company)):
		if outcome[i]:
			if not len(dates[i].split()) > 1:
				date = datetime.strptime(dates[i].get_text(), '%m/%d/%Y')
			else:
				date = datetime.strptime(dates[i].split()[1:].get_text(), '%b %Y')

			df_data.append([date, company[i].get_text(), events[i].get_text(), outcome[i].get_text()])
		else:
			df_data.append([company[i].get_text(), events[i].get_text(), outcome[i]])

	# FDA trials
	df = pd.DataFrame(df_data, columns=['Date', 'Company Name', 'Event', 'Outcome'])
	# ?PageNum=4 to ?PageNum=1
	return df

def _big_money(ticker): # Returns recent institutional investments in a stock, as well as the largest shareholders and mutual funds holding the stock
	BASE_URL = f'https://money.cnn.com/quote/shareholders/shareholders.html?symb={ticker}&subView=institutional'
	soup = _get_soup(BASE_URL)

	# Latest institutional activity
	table = soup.find('table', {'class', 'wsod_dataTable wsod_dataTableBig'})
	rows = table.find_all('tr')
	print('Recent large purchases:')
	for row in rows:
		date = row.find('td', {'class': 'wsod_activityDate'})
		info = row.find('td', {'class': 'wsod_activityDetail'})
		print(date.get_text(), info.get_text()) # Could make a data frame

	# Top 10 Owners of {Ticker}
	table = soup.find('table', {'class': 'wsod_dataTable wsod_dataTableBig wsod_institutionalTop10'})
	rows = table.find_all('tr')[1:]
	df_data = []
	for row in rows:
		data = row.find_all('td')
		df_data.append([i.get_text() for i in data])

	owners_df = pd.DataFrame(df_data, columns=['Stockholder', 'Stake', 'Shares owned', 'Total value($)', 'Shares bought / sold', 'Total change'])

	# Top 10 Mutual Funds Holding {Ticker}
	table = soup.find_all('table', {'class': 'wsod_dataTable wsod_dataTableBig wsod_institutionalTop10'})[1]
	rows = table.find_all('tr')[1:]
	df_data = []
	for row in rows:
		data = row.find_all('td')
		df_data.append([i.get_text() for i in data])

	mutual_funds_df = pd.DataFrame(df_data, columns=['Stockholder', 'Stake', 'Shares owned', 'Total value($)', 'Shares bought / sold', 'Total change'])

	BASE_URL = f'https://fintel.io/so/us/{ticker}'
	soup = _get_soup(BASE_URL)
	table = soup.find('table', {'id': 'transactions'})

	rows = table.find_all('tr')
	df_data = []
	for row in rows[1:]:
		date, form, investor, _, opt, avgshareprice, shares, shareschanged, value, valuechanged, _, _, _ = [i.get_text() for i in row.find_all('td')]
		df_data.append([date, form, investor, opt, avgshareprice, shares, shareschanged, value, valuechanged])

	recent_purchases_df = pd.DataFrame(df_data, columns=['Date', 'Form', 'Investor', 'Opt', 'Avg Share Price',
		'Shares', 'Shares Changed (%)', 'Value ($1000)', 'Value Changed (%)'])
	recent_purchases_df = recent_purchases_df.set_index('Date').sort_index(ascending=False)

	return owners_df, mutual_funds_df, recent_purchases_df.tail()

ticker = 'PLTR'
'''_get_summary(ticker), _basic_stats(ticker), _price_target(ticker), _price_predictions(ticker), 
_ta_indictators(ticker), _news_sentiments(ticker), _financials(ticker), _short_selling(ticker), 
_put_call_ratio(ticker), _find_competition(ticker), _etfs(ticker), _insider_trading(ticker)'''
print(_social_media_sentiment(ticker), _big_money(ticker))