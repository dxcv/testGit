# -*- coding: UTF-8 -*-
import tushare as ts
from datetime import datetime, date, time
import pandas as pd


# 单例
class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class TushareApi(Singleton):
    pro = ts.pro_api('a86f76280fd480e6fef6cbc434410f49f9208a596f2925d9fcc5b3c4')


def pro_adj_bar(ts_code='', start_date='', end_date='', freq='D'):
    fcts = TushareApi.pro.adj_factor(ts_code=ts_code)
    return ts.pro_bar(ts_code=ts_code, api=TushareApi.pro, adj='qfq', freq=freq, start_date=start_date,
                      end_date=end_date, fcts=fcts)


if __name__ == '__main__':
    df = TushareApi.pro.top10_holders(ts_code='600000.SH', start_date='20190101', end_date='20191231')
    df.to_csv("abc.csv")
