#!/usr/bin/env python3

from flask import Blueprint, render_template, request

controller = Blueprint('research',__name__,url_prefix='/research')

@controller.route('/',methods=['GET','POST'])
def show_dashboard():
	return render_template('research.html')


# TODO:
# 1. Create Orders History Table
