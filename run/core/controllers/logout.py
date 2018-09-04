#!/usr/bin/env python3

from flask import Blueprint, render_template, request

controller = Blueprint('logout',__name__,url_prefix='/logout')

@controller.route('/',methods=['GET','POST'])
def show_dashboard():
	return render_template('logout.html')


# TODO:
# 1. Create Orders History Table


