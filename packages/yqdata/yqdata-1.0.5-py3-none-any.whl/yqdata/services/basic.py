# -*- coding: UTF-8 -*-
# Author: Hu Min
# Date: 2021-11-30
import pandas as pd
from pandas import json_normalize
import logging
import logging.config
from yqdata.utils.opensearch import get_client
import json

def daily_basic(ts_code=None, trade_date = None, start_date=None, end_date=None):
    """
    获取每日指标数据
    :param ts_code: 股票代码
    :param trade_date: 交易日期 
    :param start_date: 开始日期 (YYYYMMDD)
    :param end_date: 结束日期 (YYYYMMDD)
    :return:
    """
    logging.debug("get daily basic, ts_code: %s, trade_date: %s, start_date: %s, end_date: %s", ts_code, trade_date, start_date, end_date)
    query = []
    if ts_code is not None:
        query.append({"match": {"ts_code.keyword":  ts_code }})
    if trade_date is not None:
        query.append({"match": {"trade_date": trade_date}})
    if start_date is not None and end_date is not None:
        query.append({"range": {"trade_date": {"gte":  start_date, "lte":  end_date}}})
    elif start_date is not None and end_date is None:
        query.append({"range": {"trade_date": {"gte":  start_date}}})
    elif start_date is None and end_date is not None:
        query.append({"range": {"trade_date": {"lte":  end_date}}})

    print(query)
    logging.info(json.dumps(query))
    return get_client().search_by_condition(index='daily_basic', must=query, size=100000)

if __name__ == '__main__':
    print(daily_basic(ts_code='000001.SZ', trade_date='20190401'))