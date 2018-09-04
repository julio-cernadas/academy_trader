#!/usr/bin/env python3
import sqlite3

connection = sqlite3.connect('master.db',check_same_thread=False)
cursor     = connection.cursor()

cursor.execute(
    """CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(16) UNIQUE,
        password VARCHAR(32),
        balance FLOAT,
        borrowed FLOAT
    );"""
)

cursor.execute(
    """CREATE TABLE bal_logs(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        unix_time FLOAT,
        balance FLOAT,
        username VARCHAR(16),
            FOREIGN KEY(username) REFERENCES users(username)
    );"""
)
cursor.execute(
    """CREATE TABLE holdings(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker VARCHAR,
        shares INTEGER,
        vwap FLOAT,
        type VARCHAR(8),
        username VARCHAR(16),
        	FOREIGN KEY(username) REFERENCES users(username)
    );"""
)

cursor.execute(
    """CREATE TABLE orders(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        unix_time FLOAT,
        ticker VARCHAR,
        shares INTEGER,
        price FLOAT,
        type VARCHAR(8),
        username VARCHAR(16),
            FOREIGN KEY(username) REFERENCES users(username)
    );"""
)

cursor.close()
connection.close()