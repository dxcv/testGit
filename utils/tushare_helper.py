# -*- coding: UTF-8 -*-
import tushare as ts
from datetime import datetime, date, time
import pandas as pd
import time as tt


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
    stockCodeList = TushareApi.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    list = []
    for index, row in stockCodeList.head(100).iterrows():
        df = TushareApi.pro.top10_holders(ts_code=row['ts_code'], start_date='20190101', end_date='20191231')
        df = df.head(10)[df.head(10)['holder_name'].str.contains(pat = '中国证券金融股份有限公司')]
        df.empty or list.append(df)
        (index+1) % 78 == 0 and tt.sleep(60)
    dd = pd.concat(list,ignore_index=True)
    dd.to_csv("abc.csv")
