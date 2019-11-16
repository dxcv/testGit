import requests
import random
import time
from bs4 import BeautifulSoup
import pandas as pd


def format_data(data):
    return (data or '').strip()


def get_company_detail(x):
    time.sleep(random.random())
    url = "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/" + x
    rr = requests.get(url)
    rr.encoding = 'utf-8'
    soup = BeautifulSoup(rr.text, 'lxml')
    tr_list = soup.select_one(".m-list-details > .table-info").tbody.find_all("tr", recursive=False)
    diff = 31 - len(tr_list)
    element = dict()
    element['机构诚信信息'] = len(tr_list[0].find_all("tr"))
    element['基金管理人全称(中文)'] = tr_list[2].find(id="complaint1").string.replace("&nbsp", "").strip()
    element['办公地址'] = format_data(tr_list[8].find("td", "td-content").string)
    element['注册资本'] = format_data(tr_list[9].find_all("td", "td-content")[0].string)
    element['实缴资本'] = format_data(tr_list[9].find_all("td", "td-content")[1].string)
    element['企业性质'] = format_data(tr_list[10].find_all("td", "td-content")[0].string)
    element['注册资本实缴比例'] = format_data(tr_list[10].find_all("td", "td-content")[1].string)
    element['机构类型'] = format_data(tr_list[11].find("td", "td-content").string)
    element['取得基金从业人数'] = format_data(tr_list[12].find_all("td", "td-content")[1].string)
    element['机构网址'] = format_data(tr_list[13].find("td", "td-content").string)
    element['法定代表人'] = format_data(tr_list[21 - diff].find("td", "td-content").string)
    element['机构信息最后更新时间'] = format_data(tr_list[29 - diff].find("td", "td-content").string)
    element['特别提示信息'] = format_data(tr_list[30 - diff].find("td", "td-content").string)
    element['详细信息网址'] = url
    element['产品数量(暂行前)'] = len(tr_list[26 - diff].find_all("a"))
    element['产品数量(暂行后)'] = len(tr_list[27 - diff].find_all("a"))
    product = dict()
    product['name'] = element['基金管理人全称(中文)']
    product_list = []
    product_list.extend(tr_list[26 - diff].find_all("a"))
    product_list.extend(tr_list[27 - diff].find_all("a"))
    product['product_list'] = "|".join(map(lambda s: format_data(s.string).replace("（", "(").replace("）", ")"),
                                           product_list))
    print(product['product_list'])
    return element, product


if __name__ == '__main__':
    keyword = "王"
    payload = dict() if keyword == "" else {"keyword": keyword}
    url_list = []
    is_last = False
    page = 0
    while not is_last:
        r = requests.post("http://gs.amac.org.cn/amac-infodisc/api/pof/manager", json=payload,
                          params={'page': page, 'size': 1000, 'rand': random.random()})
        dd = r.json()
        url_list.extend(map(lambda x: x['url'], dd['content']))
        is_last = dd['last']
        page += 1
        is_last or time.sleep(random.random() * 10)

    company_list = list(map(get_company_detail, url_list[0:5]))

    df = pd.DataFrame(map(lambda x: x[0], company_list))
    print(df)
    df.to_excel('requests.xlsx', index=False,
                engine='xlsxwriter',
                columns=['基金管理人全称(中文)', '办公地址', '注册资本', '实缴资本',
                         '企业性质', '注册资本实缴比例', '机构类型', '取得基金从业人数',
                         '机构网址', '法定代表人', '机构信息最后更新时间', '特别提示信息',
                         '详细信息网址', '产品数量(暂行前)', '产品数量(暂行后)', '机构诚信信息'])
    company_product = pd.DataFrame(map(lambda x: x[1], company_list))
    print(company_product)
    company_product.to_csv("product.csv")
