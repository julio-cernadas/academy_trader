#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session
from core.models.performance import market_value,portfolio_performance
from core.models.holdings import holdings,logs

controller = Blueprint('portfolio',__name__,url_prefix='/portfolio')

def info(username):
	if 'username' in session:
		username=session['username']
		balance,borrowed,p_l,mrkt_val,margin_remaining = portfolio_performance(username,'LONG','SHORT')
		h_list = holdings(username)
		return render_template('portfolio.html',
								username = username,
								balance  = balance,
								borrowed = borrowed,
								mrkt_val = mrkt_val,
								p_l      = p_l,
								h_list   = h_list,
								margin_remaining = margin_remaining)

@controller.route('/',methods=['GET','POST'])
def dashboard():
	return info(session['username'])