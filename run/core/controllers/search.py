#!/usr/bin/env python3
from flask import Blueprint, render_template, request, session
from core.models.searching import search_api

controller = Blueprint('search',__name__,url_prefix='/search')

@controller.route('/',methods=['GET','POST'])
def show_dashboard():
	if request.method == 'GET':
		if 'username' in session:
			username=session['username']
			search = request.args.get('search')
			lst,ticker = search_api(search)
			return render_template('search.html',
									username = username,
									ticker  = f'{ticker}',
									lst = lst)