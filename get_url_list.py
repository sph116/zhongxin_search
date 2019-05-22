from lxml import etree
import pymysql
from request_model import request1
import requests
from mysql_module import mysql

# host = "localhost"
# user = "sph"
# password = "123456"
# db = "spider"
# port = 3306
# table = 'zx_search'

def Get_url_list(param, Tread_name):
    print(Tread_name + "：启动")
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'}
    for i in range(0, param, 100):
        data = {
            'q': '的',               #搜索条件int ‘的’来搜索绝大多数新闻
            'ps': 100,               #每页100条数据
            'start': i,              #翻页参数 每翻一页加100
            'type': '',
            'sort': 'pubtime',
            'time_scope': '365',
            'channel': 'all',
            'adv': '1',
            'day1': '',
            'day2': '',
            'field': 'content',
            'creator': '',
        }

        start_url = 'http://sou.chinanews.com/search.do'
        try:
            rep = request1.get(start_url, data, 5)
            # rep = requests.post(url=start_url, headers=headers, data=data, timeout=5)
            if rep.status_code == 200:
                parse(rep, i)
        except Exception as e:
            print(Tread_name, ':链接失败', param, '原因:', e)

def parse(rep, i):

    rep.encoding = rep.apparent_encoding      #解决编码问题
    # con = rep.content
    # sel = html.fromstring(con)
    sel = etree.HTML(rep.text)
    # print(rep.text)
    url_lists = sel.xpath('//div[@id="news_list"]/table//tr[1]/td[2]/ul/li[1]/a/@href')       #从列表页提取详情页列表
    mysql.save_url(url_lists, i)

# def save_mysql(url_lists, i):
#     db = pymysql.connect(host=host, user=user,
#                          password=password, db=db, port=port)
#     cur = db.cursor()
#
#     for url in url_lists:
#         item = {
#             'state': '1',   #所有url 入库状态字典写为1 为未爬取状态
#             'url': url,
#         }
#
#         table = table
#         keys = ', '.join(item.keys())
#         values = ', '.join(['%s'] * len(item))
#         sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys,
#                                                                      values=values)
#         try:
#             if cur.execute(sql, tuple(item.values())):
#                 db.commit()
#
#
#         except Exception as a:
#             print(':插入数据失败, 原因', a)
#             db.rollback()
#     index = i/100 + 1  #详情页页码
#     print(str(index) + '页url数据插入成功')











