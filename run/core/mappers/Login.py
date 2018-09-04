#!/usr/bin/env/ python3

from core.mappers.Connections import Select

class Login(Select):
	def __init__(self, username, password):
		self.username = username
		self.password = password
	
	def check_account(self):
		return self.check_existing_account(self.username,self.password)
