#!/usr/bin/env python3
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session

from core.mappers.User  import User
from core.mappers.Login import Login
from core.models.trade  import log_transaction
controller = Blueprint('index',__name__,url_prefix='')


@controller.route('/',methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = Login(username,password)
		x = user.check_account()
		if x == None:
			return render_template('login.html')
		else:
			session['username'] = username
			return redirect(url_for('portfolio.dashboard'))
		## New to improve this as well, at least build upon it!


@controller.route('/signup',methods=['GET','POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		new_user = User(username,password,100000,0)
		new_user.create_user()
		unix = datetime.datetime.utcnow().timestamp()
		log_transaction(unix,username)
		return redirect('/')
