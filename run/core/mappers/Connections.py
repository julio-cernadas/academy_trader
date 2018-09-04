#!/usr/bin/env python3
import sqlite3
import pandas as pd
from core.mappers.Base import Base


## SELECTS ###
class Select(Base):
	def check_existing_account(self,username,password):
		sql_cmd = """SELECT username,password FROM users WHERE username='{}'
							AND password='{}';""".format(username,password)
		try:
			username = self.connect_fetch(sql_cmd)
			return username
		except IndexError:
			return None

	def check_admin(self,username,password):
		sql_cmd = """SELECT username,password FROM users WHERE username='{}'
							AND password='{}';""".format(username,password)
		try:
			username = self.connect_fetch(sql_cmd)
			return username
		except IndexError:
			return None

	def select_balance(self,username):
		sql_cmd = 'SELECT balance FROM users WHERE username="{0}";'.format(username)
		items = self.connect_fetch(sql_cmd)
		return items

	def select_borrowed(self,username):
		sql_cmd = 'SELECT borrowed FROM users WHERE username="{0}";'.format(username)
		items = self.connect_fetch(sql_cmd)
		return items

	def select_ticker(self,ticker,username,type):
		sql_cmd = 	"""SELECT ticker 
					FROM holdings 
					WHERE ticker='{0}' 
					AND username='{1}'
					AND type='{2}';""".format(ticker,username,type)
		try:
			tickers = self.connect_fetch(sql_cmd)
			return tickers
		except IndexError:
			return None

	def select_mrkt_val(self,username,type1):
		sql_cmd = 	"""	SELECT ticker,shares FROM holdings
						WHERE username='{0}' and type='{1}';""".format(username,type1)
		items = [i for i in self.connect_multi(sql_cmd)]
		return items

	def select_shrt_val(self,username,type2):
		sql_cmd = 	"""	SELECT ticker,shares FROM holdings
						WHERE username='{0}' and type='{1}';""".format(username,type2)
		items = [i for i in self.connect_multi(sql_cmd)]
		return items
	
	def select_holding(self,ticker,username,type):
		sql_cmd = """SELECT shares,vwap
					FROM holdings 
					WHERE ticker='{0}' AND 
					username='{1}' AND
					type='{2}';""".format(ticker,username,type)
		items = [i for i in self.connect_list(sql_cmd)]
		return items

	def select_all_holdings(self,username):
		sql_cmd =	"""SELECT ticker,type,shares,vwap
						FROM holdings 
						WHERE username='{0}';
				 	""".format(username)
		items = [i for i in self.connect_multi(sql_cmd)]
		return items

	def select_all_orders(self,username):
		sql_cmd = 	"""SELECT unix_time,ticker,type,shares,price
						FROM orders 
						WHERE username='{0}';
					""".format(username)
		items = [i for i in self.connect_multi(sql_cmd)]
		return items

	def select_all_logs(self,username):
		sql_cmd = 	"""SELECT unix_time,balance
						FROM bal_logs 
						WHERE username='{0}';
					""".format(username)
		items = [i for i in self.connect_multi(sql_cmd)]
		return items

	# def select_leaderboards(self):
	# 	connection = connect_commit()
	# 	df = pd.read_sql_query(
	# 		"""SELECT username,balance,mrkt_val
	# 			FROM users
	# 			WHERE balance > 0
	# 			ORDER BY mrkt_val DESC
	# 			LIMIT 10;""",connection)
	# 	connection.close
	# 	return df


# ____________________ INSERTS ____________________ #
class Insert(Base):
	def insert_to_orders(self,unix,ticker,shares,last_price,type,username):
		sql_cmd = """INSERT INTO orders(
					unix_time,ticker,shares,price,type,username)
					VALUES({0},'{1}',{2},{3},'{4}','{5}');""".format(
					unix,ticker,shares,last_price,type,username)
		self.connect(sql_cmd)

	def insert_to_holdings(self,ticker,shares,last_price,type,username):
		sql_cmd = """INSERT INTO holdings(
					ticker,shares,vwap,type,username)
					VALUES('{0}',{1},{2},'{3}','{4}');""".format(ticker,shares,last_price,type,username)
		self.connect(sql_cmd)

	def insert_account(self,username,password,balance,borrowed):
		sql_cmd = """INSERT INTO users(
				    username, password, balance, borrowed) 
					VALUES('{}','{}',{},{});
					""".format(username, password, balance, borrowed)
		self.connect(sql_cmd)

	def insert_log(self,unix_time,balance,username):
		sql_cmd = 	""" INSERT INTO bal_logs(
						unix_time,balance,username)
						VALUES({},{},'{}');
					""".format(unix_time,balance,username)
		self.connect(sql_cmd)

	### UPDATES SEG ###
	def update_holdings(self,total_vol,new_vwap,ticker,username,type):
		sql_cmd = """UPDATE holdings 
					SET shares={0},vwap={1}
					WHERE ticker='{2}' AND 
					username='{3}' AND
					type='{4}';""".format(
					total_vol,new_vwap,ticker,username,type)
		self.connect(sql_cmd)

	def update_balance(self,new_balance,username):
		sql_cmd = """UPDATE users SET balance={0}
					WHERE username='{1}';""".format(
					new_balance,username)
		self.connect(sql_cmd)

	def update_borrowed(self,new_borrowed,username):
		sql_cmd = """UPDATE users SET borrowed={0}
					WHERE username='{1}';""".format(
					new_borrowed,username)
		self.connect(sql_cmd)


# ____________________ DELETES ____________________ #
class Delete(Base):
	def delete_holding(self,ticker,username,type):
		sql_cmd ='''SELECT rowid 
					FROM holdings 
					WHERE ticker="{0}" AND 
					username="{1}" AND
					type='{2}';'''.format(ticker,username,type)
		id = self.connect_fetch(sql_cmd)
		sql_cmd = 'DELETE FROM holdings WHERE rowid={0};'.format(id,)
		self.connect(sql_cmd)

	# def delete_user(username):
	# 	connection = connect_commit()
	# 	cursor = connection.cursor()
	# 	cursor.execute('SELECT rowid FROM users WHERE username="{0}";'.format(username))
	# 	try:
	# 		id = cursor.fetchall()[0][0]
	# 		cursor.execute('DELETE FROM users WHERE rowid={0};'.format(id,))
	# 		connection.commit()
	# 		cursor.close()
	# 		connection.close()
	# 		return 'Success'
	# 	except IndexError:
	# 		return None
