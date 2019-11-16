import jqdatasdk
from jqdatasdk import finance
import pandas as pd

if __name__ == '__main__':
    jqdatasdk.auth("13234097668", "Abc13234097668")
    stocks = list(jqdatasdk.get_all_securities(['stock']).index)
    top10_or_list = []
    top10_and_list = []
    for code in stocks:
        q = jqdatasdk.query(finance.STK_SHAREHOLDER_TOP10).filter(finance.STK_SHAREHOLDER_TOP10.code == code,
                                                                  finance.STK_SHAREHOLDER_TOP10.pub_date > '2019-01-01')
        search = ['中国证券金融股份有限公司', '香港中央结算']
        df = finance.run_query(q).tail(10)
        df = df[df['shareholder_name'].str.contains(pat='|'.join(str(v) for v in search))]
        df.empty or top10_or_list.append(df)
        len(df.index) >= len(search) and top10_and_list.append(df.head(1))
    writer = pd.ExcelWriter('output.xlsx')
    len(top10_or_list) == 0 or pd.concat(top10_or_list, ignore_index=True).rename(
        columns={'code': '代码', 'company_name': '名称', 'shareholder_name': '股东名称', 'shareholder_rank': '股东名次',
                 'shareholder_class': '股东类别', 'share_number': '持股数量', 'share_ratio': '持股比例',
                 'pub_date': '公告日期', 'end_date': '截止日期', 'sharesnature': '股份性质',
                 'share_pledge_freeze': '股份质押冻结数量',
                 'share_pledge': '股份质押数量', 'share_freeze': '股份冻结数量'}).to_excel(writer, sheet_name='分散', index=False,
                                                                               engine='xlsxwriter',
                                                                               columns=['代码', '名称', '股东名称', '股东名次',
                                                                                        '股东类别', '持股数量', '持股比例', '公告日期',
                                                                                        '截止日期', '股份性质', '股份质押冻结数量',
                                                                                        '股份质押数量', '股份冻结数量'])
    len(top10_and_list) == 0 or pd.concat(top10_and_list, ignore_index=True).rename(
        columns={'code': '代码', 'company_name': '名称',
                 'pub_date': '公告日期', 'end_date': '截止日期'}).to_excel(writer, sheet_name='合并', index=False,
                                                                   engine='xlsxwriter',
                                                                   columns=['代码', '名称', '公告日期', '截止日期'])
    writer.save()
