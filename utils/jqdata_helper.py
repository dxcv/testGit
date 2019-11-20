import jqdatasdk
from jqdatasdk import finance
import pandas as pd
import time
import os


def load_top10_data(fun=(lambda x: x), ext="all", force=False):
    path = "top10_data_%s_%s.csv" % (ext, time.strftime("%Y-%m-%d", time.localtime()))
    if not force and os.path.exists(path):
        return pd.read_csv(path)
    else:
        jqdatasdk.auth("13234097668", "Abc13234097668")
        stocks = list(jqdatasdk.get_all_securities(['stock']).index)
        df_list = []
        for code in stocks:
            query = jqdatasdk.query(finance.STK_SHAREHOLDER_TOP10).filter(finance.STK_SHAREHOLDER_TOP10.code == code,
                                                                          finance.STK_SHAREHOLDER_TOP10.pub_date > '2019-01-01')
            df_list.append(fun(finance.run_query(query)))
        top10_data = pd.concat(df_list, ignore_index=True)
        top10_data.to_csv(path, index=False)
        return top10_data


def load_top10_to_excel(*search):
    top10_data = load_top10_data(lambda x: x.tail(10), "newest", False)
    top10_or_list = top10_data[top10_data['shareholder_name'].str.contains(
        pat='|'.join(str(v) for v in search))]
    itemCount = top10_or_list['code'].groupby(top10_or_list['code']).count()
    top10_and_list = top10_or_list[top10_or_list['code'].isin(itemCount[itemCount >= len(search)].index.values)]
    columns1 = {'code': '代码', 'company_name': '名称', 'shareholder_name': '股东名称', 'shareholder_rank': '股东名次',
                'shareholder_class': '股东类别', 'share_number': '持股数量', 'share_ratio': '持股比例',
                'pub_date': '公告日期', 'end_date': '截止日期', 'sharesnature': '股份性质',
                'share_pledge_freeze': '股份质押冻结数量',
                'share_pledge': '股份质押数量', 'share_freeze': '股份冻结数量'}
    columns2 = {'code': '代码', 'company_name': '名称', 'pub_date': '公告日期', 'end_date': '截止日期'}

    writer = pd.ExcelWriter('output.xlsx')
    top10_or_list.rename(columns=columns1).to_excel(writer, sheet_name='分散', index=False, engine='xlsxwriter',
                                                    columns=['代码', '名称', '股东名称', '股东名次',
                                                             '股东类别', '持股数量', '持股比例', '公告日期',
                                                             '截止日期', '股份性质', '股份质押冻结数量',
                                                             '股份质押数量', '股份冻结数量'])
    top10_and_list.rename(columns=columns2).to_excel(writer, sheet_name='合并', index=False, engine='xlsxwriter',
                                                     columns=['代码', '名称', '公告日期', '截止日期'])
    writer.save()


if __name__ == '__main__':
    load_top10_to_excel('中国证券金融股份有限公司', '香港中央结算')
