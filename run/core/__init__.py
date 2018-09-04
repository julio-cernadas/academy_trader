 #!/usr/bin/env python3
import os
from flask import Flask

from core.controllers.index import controller as index
from core.controllers.portfolio import controller as portfolio
from core.controllers.trade import controller as trade
from core.controllers.orders import controller as orders
from core.controllers.research import controller as research
from core.controllers.logout import controller as logout
from core.controllers.search import controller as search

def keymaker(app,filename='secret_key'):
	pathname=os.path.join(app.instance_path,filename)
	try:
		app.config['SECRET_KEY'] = open(pathname,'rb').read()
	except IOError:
		parent_directory = os.path.dirname(pathname)
		if not os.path.isdir(parent_directory):
			os.system('mkdir -p {}'.format(parent_directory))
		os.system('head -c 24 /dev/urandom > {}'.format(pathname))
		app.config['SECRET_KEY'] = open(pathname,'rb').read()

app = Flask(__name__)

app.register_blueprint(index)
app.register_blueprint(portfolio)
app.register_blueprint(trade)
app.register_blueprint(orders)
app.register_blueprint(research)
app.register_blueprint(logout)
app.register_blueprint(search)

keymaker(app)