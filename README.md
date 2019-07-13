# zhongxin_search
# 中国新闻网爬虫

中国新闻网高级搜索接口爬虫  http://sou.chinanews.com/search.do?q=%E7%9A%84  搜索关键字 “的” （详情页数量600万）

可用时间至2019.7.13

已集成多线程，url查重，异常更换代理，翻页，错误信息存储（10线程每日抓取数量为15万-20万左右）。

适用于文本分析，文本分类。词向量提取

# 环境：
  py3.7

# 第三方库：
  requests pymysql lxml

# 功能模块：
* Spider_action 多线程调度以及程序启动

* save_text 文本分类存储

* request_model 请求模块，异常重试或使用代理

* ip_pool 代理池维护模块

* get_url_list 列表页请求模块

* get_detail_page 详情页请求模块

* mysql_model 数据库增删改查


# 注：
* 过于久远的详情页页面规则会改动，需要自行维护。

* 需更换ip_poll模块下代理api

* 需要更换mysql_model 数据库信息

* 列表页抓取未完成查重，需要每次启动定义post请求参数（翻页参数为页数*100，增量）

* 启动Spider_action_detail会自动创建相关数据库及文本路径信息
