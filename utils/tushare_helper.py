# -*- coding: UTF-8 -*-
import tushare as ts
from datetime import datetime, date, time


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
    dd = ts.pro_bar(ts_code='300408.SZ', api=TushareApi.pro, adj='qfq', freq="1MIN", start_date="20191023",
                      end_date="20191024")

    df =pro_adj_bar(ts_code='300408.SZ')
    df['Adj Close'] = df['close']
    df = df.rename(
        columns={'trade_date': 'Date Time', 'open': 'Open', 'high': 'High', 'vol': 'Volume', 'close': 'Close',
                 'low': 'Low'})
    print(df[['Date Time', 'Open', 'High', 'Volume','Close','Low','Adj Close']])

    print(df.info())
    print(df.head())
