#!/usr/bin/env/ python3

from core.mappers.Connections import Insert

class User(Insert):
	def __init__(self, username, password, balance, borrowed):
		self.username = username
		self.password = password
		self.balance = balance
		self.borrowed = borrowed
		
	def create_user(self):
		return self.insert_account(self.username,self.password,self.balance,self.borrowed)
	