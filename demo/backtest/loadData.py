import tushare as ts
import pandas as pd
import time

if __name__ == '__main__':
    stock_code = '300408.SZ'
    pro = ts.pro_api('a86f76280fd480e6fef6cbc434410f49f9208a596f2925d9fcc5b3c4')

    fcts = pro.adj_factor(ts_code=stock_code, start_date='20110101', end_date='20200101')[['trade_date', 'adj_factor']]
    # dd.to_csv("../../api/stock/csv/adj.csv")
    year_list = []
    for i in range(2019, 2014, -1):
        df1 = ts.pro_bar(ts_code=stock_code, api=pro, adj='qfq', freq="5MIN", start_date=str(i) + '0101',
                         end_date=str(i) + '0601', fcts=fcts)
        df2 = ts.pro_bar(ts_code=stock_code, api=pro, adj='qfq', freq="5MIN", start_date=str(i) + '0601',
                         end_date=str(i + 1) + '0101', fcts=fcts)
        year_list.append(df2)
        year_list.append(df1)
        if i % 2 == 0:
            time.sleep(60)

    df = pd.concat(year_list, ignore_index=True)

    df['Adj Close'] = df['close']
    df = df.rename(
        columns={'trade_time': 'Date Time', 'open': 'Open', 'high': 'High', 'vol': 'Volume', 'close': 'Close',
                 'low': 'Low'})
    print(df.info())
    print(df.head())
    print(df.tail())
    # df.index = df['Date Time']
    # df.index.name = 'date'
    # print(df.head())
    df.to_csv("../../api/stock/csv/%s_5min.csv" % stock_code.replace('.', ''),
              columns=['Date Time', 'Open', 'High', 'Volume', 'Close', 'Low', 'Adj Close'], index=False)
