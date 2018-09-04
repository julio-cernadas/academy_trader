#!/usr/bin/env/ python3
import json
import requests

def get_last_price(ticker):
	url = "https://www.alphavantage.co/query"
	function = "TIME_SERIES_INTRADAY"
	symbol = ticker
	interval = "1min"
	outputsize= "compact"
	api_key = "4I16NYFU17Q3KNKC"
	data = { "function": function,
			"symbol": symbol,
			"interval": interval,
			"outputsize": outputsize,
			"apikey": api_key }
	try: 
		# MarkitOnDemand  Attempt - 1 
		endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='+ticker
		response = requests.get(endpoint).json()
		last_price = response['LastPrice']
		return last_price	
	except:
		try:
			# AlphaVantage    Attempt - 2 
			dictionary = requests.get(url, params = data).json() 
			keys = list(dictionary.keys())
			series = keys[1]
			resp = dictionary[series]
			dict_ = next(iter(resp.values()))
			last_price = dict_['1. open']
			return float(last_price)
		except:
			return None

def get_company_name(ticker):
	try:
		endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='+ticker
		response = requests.get(endpoint).json()
		company_name = response['Name']
		return company_name
	except:
		return 'N/A'

def get_info_from_request(search):
	endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input='+search
	# TODO Re-factor the following code so it doesn't just arbitrarily take the first
	#      thing in the iterable that's returned and assume it's the security we want
	response = requests.get(endpoint).json()[0]
	try:
		ticker = response['Symbol']
		company_name = response['Name']
		exchange = response['Exchange']
		return ticker,company_name,exchange
	except:
		return 'N/A','N/A','N/A'

def get_info_from_result(ticker):
	endpoint   = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='+ticker
	try:
		response   = requests.get(endpoint).json()
		last_price = response['LastPrice']
		change     = response['ChangePercent']
		market_cap = response['MarketCap']
		volume     = response['Volume']
		ytd        = response['ChangeYTD']
		ytd_percnt = response['ChangePercentYTD']
		return last_price,change,market_cap,volume,ytd,ytd_percnt
	except:
		return 'N/A','N/A','N/A','N/A','N/A','N/A'