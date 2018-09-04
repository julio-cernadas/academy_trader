#!/usr/bin/env python3
import datetime

from core.mappers.Connections import Select, Insert, Delete
from core.wrapper.wrapper import get_last_price 


def buy(ticker, shares, type, username):
    last_price = get_last_price(ticker)
    if last_price != None:
        # ______ Set Variables ______ #
        shares = float(shares)
        user_balance = Select().select_balance(username)
        fee = 3.00
        transaction_cost = (last_price * shares) + fee
        # ______ Execute Trade ______ #
        if user_balance >= transaction_cost:
            result = Select().select_ticker(ticker,username,type)
            if result == None:
                # If the holding DOESN'T exist. Add holding...
                Insert().insert_to_holdings(ticker,shares,
                                            last_price,type,username)
            else:               
                # If it DOES exist, then Modify the holding...
                items = Select().select_holding(ticker,username,type)
                prev_shares = float(items[0])
                prev_price = float(items[1])
                curr_shares = shares
                # Adjustment Calculations...
                old = prev_shares * prev_price
                new = curr_shares * last_price
                total_vol = prev_shares + curr_shares
                new_vwap = (old + new) / (total_vol)
                Insert().update_holdings(total_vol,new_vwap,ticker,username,type)
            # ______ Update Database ______ #
            unix = datetime.datetime.utcnow().timestamp()
            Insert().insert_to_orders(unix,ticker,shares,last_price,type,username)
            new_balance = user_balance - transaction_cost
            Insert().update_balance(new_balance,username)
            log_transaction(unix,username)
        else:
            # ______ Avoid Trade ______ #
            return 'Error: Not Enough Funds!'
    else:
        # ______ Avoid Trade ______ #
        return 'Error: No Ticker Match!'

def sell(ticker, shares, type, username):
    # ______ Execute Trade ______ #
    result = Select().select_ticker(ticker,username,type)
    if result != None: 
        # If ticker in holdings table...
        # ______ Set Variables ______ #
        items = Select().select_holding(ticker,username,type)
        prev_shares = float(items[0])
        prev_price = float(items[1])
        curr_shares = float(shares)
        last_price = get_last_price(ticker)
        fee = 3.00
        user_balance = Select().select_balance(username)
        transaction_prof = (last_price * curr_shares) - fee
        new_balance = user_balance + transaction_prof
        if prev_shares > curr_shares:
            old = prev_shares * prev_price
            new = curr_shares * last_price
            total_vol = prev_shares - curr_shares
            new_vwap = (old - new) / (total_vol)
            Insert().update_holdings(total_vol,new_vwap,ticker,username,type)
            Insert().update_balance(new_balance,username)
            unix = datetime.datetime.utcnow().timestamp()
            Insert().insert_to_orders(unix,ticker,shares,last_price,'SALE',username)
            log_transaction(unix,username)
        elif prev_shares == curr_shares:
            Delete().delete_holding(ticker,username,type)
            Insert().update_balance(new_balance,username)
            unix = datetime.datetime.utcnow().timestamp()
            Insert().insert_to_orders(unix,ticker,shares,last_price,'SALE',username)
            log_transaction(unix,username)
        elif prev_shares < curr_shares:
            return 'Error: Not Enough Shares!'
    else:
        # ______ Avoid Trade ______ #
        return 'Error: Not In Holdings!'

def short(ticker, shares, type, username):
    last_price = get_last_price(ticker)
    if last_price != None:
        # ______ Set Variables ______ #
        borrowed = Select().select_borrowed(username)
        user_balance = Select().select_balance(username)
        fee = 3.00
        curr_shares = float(shares)
        transaction_loan = last_price * curr_shares
        # ______ Execute Trade ______ #
        if borrowed <= user_balance and user_balance >= transaction_loan:
            result = Select().select_ticker(ticker,username,type)
            if result == None:
                # If the holding DOESN'T exist. Add holding...
                Insert().insert_to_holdings(ticker,curr_shares,
                                            last_price,type,username)
            else:  
                # If it DOES exist, then make sure its not a 'LONG'...
                items = Select().select_holding(ticker,username,type)
                prev_shares = float(items[0])
                prev_price  = float(items[1])
                # Adjustment Calculations...
                old = prev_shares * prev_price
                new = curr_shares * last_price
                total_vol = prev_shares + curr_shares
                new_vwap  = (old + new) / (total_vol)
                Insert().update_holdings(total_vol,new_vwap,ticker,username,type)
            # ______ Update Database ______ #
            unix = datetime.datetime.utcnow().timestamp()
            Insert().insert_to_orders(unix,ticker,shares,last_price,type,username)
            new_borrowed = borrowed + transaction_loan
            new_balance = user_balance - fee
            Insert().update_balance(new_balance,username)
            Insert().update_borrowed(new_borrowed,username)
            log_transaction(unix,username)
        else:
            # ______ Avoid Trade ______ #
            return 'Error: Not Enough Funds To Short!'

    else:
        # ______ Avoid Trade ______ #
        return 'Error: No Ticker Match!'

def cover(ticker, shares, type, username):
    # ______ Execute Trade ______ #
    result = Select().select_ticker(ticker,username,type)
    if result != None: 
        # ______ Set Variables ______ #
        items = Select().select_holding(ticker,username,type)
        prev_shares = float(items[0])
        prev_price  = float(items[1])
        curr_shares = float(shares)
        last_price  = get_last_price(ticker)
        fee         = 3.00
        # ______ Adjust Balances ______ #
        user_balance = Select().select_balance(username)
        borrowed     = Select().select_borrowed(username)
        position_val     = prev_price * prev_shares 
        transaction_cost = last_price * curr_shares
        new_balance      = user_balance + (position_val - transaction_cost) - fee
        new_borrowed     = borrowed - transaction_cost

        if prev_shares > curr_shares:
            old = prev_shares * prev_price
            new = curr_shares * last_price
            total_vol = prev_shares - curr_shares
            new_vwap = (old - new) / (total_vol)
            Insert().update_holdings(total_vol,new_vwap,ticker,username,type)
            Insert().update_balance(new_balance,username)
            Insert().update_borrowed(new_borrowed,username)
            unix = datetime.datetime.utcnow().timestamp()
            Insert().insert_to_orders(unix,ticker,shares,last_price,'COVER',username)
            log_transaction(unix,username)
        elif prev_shares == curr_shares:
            Delete().delete_holding(ticker,username,type)
            Insert().update_balance(new_balance,username)
            Insert().update_borrowed(new_borrowed,username)
            unix = datetime.datetime.utcnow().timestamp()
            Insert().insert_to_orders(unix,ticker,shares,last_price,'COVER',username)
            log_transaction(unix,username)
        elif prev_shares < curr_shares:
            return 'Error: Not Enough Shares!'
    else:
        # ______ Avoid Trade ______ #
        return 'Error: Not In Holdings!'

def user_balances(username):
    balance  = Select().select_balance(username)
    borrowed = Select().select_borrowed(username)
    m_r = 100000.00 - borrowed
    return f'{balance:.2f}', f'{m_r:.2f}'

def log_transaction(unix_time,username):
    balance = Select().select_balance(username)
    Insert().insert_log(unix_time,balance,username)