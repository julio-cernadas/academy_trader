#!/usr/bin/env python3
from flask import Blueprint, render_template, request, session, redirect, url_for

from core.models.trade import buy, sell, short, cover, user_balances
from core.models.holdings import holdings

controller = Blueprint('trade',__name__,url_prefix='/trade')

@controller.route('/',methods=['GET','POST'])
def show_dashboard():
	if request.method == 'GET':
		if 'username' in session:
			username=session['username']
			h_list = holdings(username)
			balance,margin_remaining = user_balances(username)
			return render_template('trade.html',
									username = username,
									balance  = balance,
									margin_remaining = margin_remaining,
									h_list   = h_list)

	elif request.method == 'POST':
		if 'username' in session:
			username=session['username']			
			ticker = request.form['ticker']
			shares = request.form['shares']
			type = request.form['type']
			if type == 'buy':
				type = 'LONG'
				buy(ticker,shares,type,username)
				return redirect(url_for('trade.show_dashboard'))
			elif type == 'sell':
				type = 'LONG'
				sell(ticker,shares,type,username)
				return redirect(url_for('trade.show_dashboard'))
			elif type == 'short':
				type = 'SHORT'
				short(ticker,shares,type,username)
				return redirect(url_for('trade.show_dashboard'))
			elif type == 'cover':
				type = 'SHORT'
				cover(ticker,shares,type,username)
				return redirect(url_for('trade.show_dashboard'))
		