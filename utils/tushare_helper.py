import tushare as ts
import pandas as pd
import time


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
    stock_code_list = TushareApi.pro.stock_basic(exchange='', list_status='L',
                                                 fields='ts_code,symbol,name,area,industry,list_date')
    top10_list = []
    for index, row in stock_code_list.iterrows():
        df = TushareApi.pro.top10_holders(ts_code=row['ts_code'], start_date='20190101', end_date='20191231')
        df = df.head(10)[df.head(10)['holder_name'].str.contains(pat='中国证券金融股份有限公司')]
        df.empty or top10_list.append(df)
        (index + 1) % 78 == 0 and time.sleep(60)
    dd = pd.concat(top10_list, ignore_index=True)
    dd = pd.merge(dd, stock_code_list)
    dd = dd.rename(columns={'symbol': '代码', 'name': '名称', 'area': '地区', 'industry': '行业', 'holder_name': '股东名称',
                            'ann_date': '发布日期', 'end_date': '结束日期',
                            'hold_amount': '持有数量', 'hold_ratio': '持有比例'})
    print(dd.info())
    dd.to_excel("output.xlsx", engine='xlsxwriter', index=False,
                columns=['代码', '名称', '地区', '行业', '股东名称', '发布日期', '结束日期', '持有数量', '持有比例'])
