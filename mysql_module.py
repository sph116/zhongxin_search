import time
import pymysql

class Operation_MySQL():

    def __init__(self):

        self.host = 'localhost'
        self.user = 'root'
        self.password = '92079320'
        self.port = 3306
        self.db = 'spider1'
        self.SQL_urlLAs = "select * from zx_search"

        try:
            con = pymysql.connect(host=self.host, user=self.user,
                                  passwd=self.password, charset='utf8')
            cur = con.cursor()
            cur.execute("create database spider1 character set utf8;")

            cur.execute("use spider1")
            cur.execute("create table zx_search(state VARCHAR(10),url VARCHAR(200))")
            cur.execute("create table zx_search_exception(url VARCHAR(100),exception VARCHAR(200))")
            print("spider1 数据库创建成功 zx_search及zx_search_exception表创建成功")
        except Exception as e:
            pass

    def save_url(self, url_lists, i):
        """存储详情页url"""
        db = pymysql.connect(host=self.host, user=self.user,
                             password=self.password, db=self.db, port=self.port)
        cur = db.cursor()

        for url in url_lists:
            item = {
                'state': '1',  # 所有url 入库状态字典写为1 为未爬取状态
                'url': url,
            }

            table = "zx_search"
            keys = ', '.join(item.keys())
            values = ', '.join(['%s'] * len(item))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys,
                                                                         values=values)
            try:
                if cur.execute(sql, tuple(item.values())):
                    db.commit()

            except Exception as a:
                print(':插入数据失败, 原因', a)
                db.rollback()
        index = i / 100 + 1  # 详情页页码
        print(str(index) + '页url数据插入成功')


    def get_data(self):

        """获取url列表"""

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        cur = db.cursor()

        sql = self.SQL_urlLAs
        try:
            cur.execute(sql)  # 执行sql语句
            date_list = []
            results = cur.fetchall()  # 获取查询的所有记录
            # 遍历结果
            date_list = [list(row)[1] for row in results if list(row)[0] == "1"]
            # for row in results:
            #     all_date = list(row)
            #     if all_date[0] == '1':  # 状态不等于二的url 需要爬取
            #         date_list.append(all_date[1])
            #     else:
            #         pass

        except Exception as e:
            print('查询失败 原因： ', e)
        # print(date_list)
        print('Thread_main' + ':url_list' + '查询成功')
        return date_list



    def get_wrong_data(self):

        """获取需重新爬取url列表"""

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        cur = db.cursor()
        wrong_list = []
        sql = self.SQL_urlLAs
        try:
            cur.execute(sql)  # 执行sql语句

            results = cur.fetchall()  # 获取查询的所有记录

            # 遍历结果

            for row in results:
                all_date = list(row)
                if all_date[0] == '5':  # 状态等于3的url 爬取失败 重新爬取
                    wrong_list.append(all_date[1])
                else:
                    pass

        except Exception as e:
            print('查询失败 原因： ', e)

        print('Thread_main' + ':wrong_list' + '查询成功')
        return wrong_list




    def Modify_Table(self, url):

        """修改本条url状态为3"""
        """3为爬取失败 不需要重新爬取"""

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        cur = db.cursor()
        cur.execute("update zx_search set state=3 WHERE url = %s", url)
        db.commit()
        db.close()

    def Modify_Table1(self, url):

        """修改本条url状态为restart"""
        """5为爬取失败 需要重新爬取"""

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        cur = db.cursor()
        cur.execute("update zx_search set state=5 WHERE url = %s", url)
        db.commit()
        db.close()

    def Modify_Table2(self, url):

        """修改本条url状态为2"""
        """2为爬取成功"""

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        cur = db.cursor()
        cur.execute("update zx_search set state=2 WHERE url = %s", url)
        db.commit()
        db.close()

    def save_exception(self, exception_date):

        """将错误信息存储"""

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db)
        cur = db.cursor()
        item = {
            'url': exception_date[0],
            'exception': exception_date[1]
        }
        # print(item)
        table = 'zx_search_exception'
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys,
                                                                     values=values)
        try:
            if cur.execute(sql, tuple(item.values())):
                db.commit()

        except Exception as a:
            db.rollback()

        db.close()
        # print('错误信息保存成功')





mysql = Operation_MySQL()

