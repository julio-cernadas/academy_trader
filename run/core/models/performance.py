#!/usr/bin/env python3
from core.mappers.Connections import Select
from core.wrapper.wrapper import get_last_price


def market_value(username,type1,type2):
    # MONEY LONGS
    lst = Select().select_mrkt_val(username,type1)
    m_v_list = []
    for ticker,shares in lst:
        last_price = get_last_price(ticker)
        m_v = last_price * shares
        m_v_list.append(m_v)
    long_total = sum(m_v_list)
    # MONEY SHORTS
    lst = Select().select_shrt_val(username,type2)
    m_v_list = []
    for ticker,shares in lst:
        last_price = get_last_price(ticker)
        m_v = last_price * shares
        m_v_list.append(m_v)
    pre_total = sum(m_v_list)
    bor = Select().select_borrowed(username)
    short_total = bor - pre_total
    total = long_total + short_total
    return total


def portfolio_performance(username,type1,type2):
    bal = Select().select_balance(username)
    bor = Select().select_borrowed(username)
    balance = round((bal),2) 
    borrowed = round((bor),2)
    m_r = 100000.00 - borrowed
    mrkt_val = round((market_value(username,type1,type2) + balance),2)
    p_l = round((mrkt_val - 100000),2)
    return f'{balance:.2f}',f'{borrowed:.2f}',f'{p_l:.2f}',f'{mrkt_val:.2f}',f'{m_r:.2f}'