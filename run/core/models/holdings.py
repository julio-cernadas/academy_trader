#!/usr/bin/env python3
import datetime
from dateutil import tz

from core.mappers.Connections import Select
from core.wrapper.wrapper import get_company_name, get_last_price

def holdings(username):
    lst = Select().select_all_holdings(username)
    h_list = []
    for ticker,type,shares,vwap in lst:
        curr_shares = float(shares)
        company_name = get_company_name(ticker)
        last_price = round((get_last_price(ticker)),2)
        if last_price != None:
            total = round((last_price * curr_shares),2)
            long_p_l  = round((total - (curr_shares * vwap)),2)
            short_p_l = round(((curr_shares * vwap) - total),2)
            h_vars = [ticker,company_name,type,shares,last_price,total,long_p_l,short_p_l]
            h_list.append(h_vars)
        else:
            last_price = 'N/A'
            total = 'N/A'
            long_p_l  = 'N/A'
            short_p_l = 'N/A'
            h_vars = [ticker,company_name,type,shares,last_price,total,long_p_l,short_p_l]
            h_list.append(h_vars)
    return h_list

def orders(username):
    lst = Select().select_all_orders(username)
    h_list = []
    for unix_time,ticker,type,shares,price in lst:
        company_name = get_company_name(ticker)
        date = datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
        total = price * float(shares)
        h_vars = [date,ticker,company_name,type,shares,price,total]
        h_list.append(h_vars)
    return reversed(h_list)

def logs(username):
    lst = Select().select_all_logs(username)
    h_list = []
    for unix_time,balance in lst:
        date = datetime.datetime.fromtimestamp(unix_time).strftime('%Y%m%d %H:%M:%S')
        h_vars = [date,balance]
        h_list.append(h_vars)
    start = h_list[ 0][0]
    start = datetime.strptime(start,'%Y%m%d %H:%M:%S')
    end   = h_list[-1][0]
    end   = datetime.strptime(end,"%Y%m%d %H:%M:%S")
    intv  = 10
    dif   = (end - start) / intv
    y = []
    for i in range(intv):
        x = (start + diff * i).strftime("%Y%m%d %H:%M:%S")
        y.append(x)
    y.append(end.strftime("%Y%m%d %H:%M:%S"))
    return y
    

# def date_range(start, end, intv):
#     start = datetime.strptime(start,"%Y%m%d %H:%M:%S")
#     end = datetime.strptime(end,"%Y%m%d %H:%M:%S")
#     diff = (end  - start ) / intv
#     for i in range(intv):
#         yield (start + diff * i).strftime("%Y%m%d %H:%M:%S")
#     yield end.strftime("%Y%m%d %H:%M:%S")



