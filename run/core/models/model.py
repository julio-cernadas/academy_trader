#!/usr/bin/env python3
import sqlite3
import pandas as pd

import wrapper # In-Use
import mapper  # Not-In-Use_Yet


def sell(ticker_symbol,trade_volume,username):
	trade_volume = float(trade_volume)
	user_balance = mapper.select_balance(username)
	ticker_symbols = mapper.select_ticker(ticker_symbol,username)
	brokerage_fee = 6.95
	last_price = wrapper.get_last_price(ticker_symbol)
	transaction_cost = (last_price*trade_volume)-brokerage_fee
	if ticker_symbols != None: # If the holding exists. Continue...
		x = mapper.select_holding(ticker_symbol,username)
		prev_volume = float(x[0])
		vwap = float(x[1])
		total_vol = prev_volume-trade_volume
		new_balance = user_balance + transaction_cost

		if prev_volume > trade_volume:
			mapper.update_holdings(total_vol,vwap,ticker_symbol,username)
			mrkt_value = market_value(username)
			new_mrkt_val = mrkt_value + new_balance
			mapper.update_balance(new_balance,new_mrkt_val,username)

		elif prev_volume == trade_volume:
			mapper.delete_holding(ticker_symbol,username)
			mrkt_value = market_value(username)
			new_mrkt_val = mrkt_value + new_balance
			mapper.update_balance(new_balance,new_mrkt_val,username)

		elif prev_volume < trade_volume:
			return 'You do not have that many shares!'
		return 'Successful!'
	else:
		return 'You do not have that stock!'


def admin_users_list():
	df1 = mapper.admin_pandas_connect()
	df = df1.drop(['pk'],axis=1)
	return df

def leaderboard():
	df1 = mapper.select_leaderboards()

	return df1
