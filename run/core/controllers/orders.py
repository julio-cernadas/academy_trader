#!/usr/bin/env python3
from flask import Blueprint, render_template, request, session
from core.models.holdings import orders

controller = Blueprint('orders',__name__,url_prefix='/orders')

@controller.route('/',methods=['GET'])
def show_dashboard():
	if request.method == 'GET':
		if 'username' in session:
			username=session['username']
			h_list = orders(username)
			return render_template('orders.html',
									username = username,
									h_list   = h_list)


