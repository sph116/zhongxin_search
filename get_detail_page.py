import traceback
from lxml import etree
from save_text import save_text
from request_model import request
import re
from mysql_module import mysql


def Get_detail_page(url, Thread_name):

    """
    获取详情页信息
    :param url:
    :param Thread_name:
    :return:
    """

    # url = 'http://www.chinanews.com/cj/shipin/cns/2017/09-29/news734846.shtml'
    # url1  = 'http://www.chinanews.com/m/kong/2018/12-26/8713078.shtml'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'}
    try:
        rep = request.get(url, 15)
        if rep.status_code == 200:

            parse(url, rep, Thread_name)
            mysql.Modify_Table2(url)       #爬取完成 设置状态为2
        # else:
        #     raise NameError

    except Exception as e:

        # print(repr(e))
        # print(type(repr(e)))

        if repr(e) == "IndexError('list index out of range',)":                #此种报错信息无用 不予保存
            mysql.Modify_Table(url)               #不需重新爬取设置状态为3
            pass
        else:

            exception_date = []                #创建错误信息列表
            exception_date.append(url)         #加入错误url

            exception_date.append(repr(e))           #加入错误原因  repr方法将返回字符串类型的错误信息及错误类型
            mysql.Modify_Table1(url)           #需重新爬取设置状态位restart
            mysql.save_exception(exception_date)   #将错误信息存入mysql
        print(Thread_name + '：链接失败' + url)
        traceback.print_exc()     #打印详细错误信息

def parse(url, rep, Thread_name):
    """
    解析页面及简易字符串处理
    :param url:
    :param rep:
    :param Thread_name:
    :return:
    """
    rep.encoding = "utf-8"

    # rep.encoding = rep.apparent_encoding  # 解决编码问题
    sel = etree.HTML(rep.text)
    # print(rep)

    """获得新闻类型 用于分类保存"""

    type  = sel.xpath('//div[@id="nav"]/a[3]/text()')
    if type == []:
        type = sel.xpath('//div[@id="nav"]/a[2]/text()')
        if type == []:
            type = '视频新闻'
        else:
            type = type[0]

    else:
        type = sel.xpath('//div[@id="nav"]/a[3]/text()')
        if type == []:
            type = '视频新闻'
        else:
            type = type[0]

    if 'shipin' in url:         #视频页面与普通页面解析规则不同 进入不同分支

        # title = sel.xpath('//div[@class="left"]/h1/text()')
        # title = title[0]

        datas = sel.xpath('//div[@class="content_desc"]/p//text()')

        if datas == []:               #另外的页面规则
            datas = sel.xpath('//div[@id="d1d"]/p//text()')
            if datas == []:
                datas = sel.xpath('//div[@class="video_con1_text_top"]/p//text()')


        if '据' in  datas[len(datas) - 1]:             #重复语句通常出现在最后一段 若出现 删除
            del[datas[len(datas) - 1]]

        new_datas = ''                      # 将文本列表转换为段落形式

        for data in datas:
            if '【同期】' in data or '责任编辑' in data or '编辑' in data or '记者' in data or '报道' in data or '【现场】' in data:        #删除无用重复段落
                pass
            else:
                new_datas = new_datas + data
        new_datas = new_datas.replace('　　', '\n　　').replace('【解说】', '')
        save_name = url.replace('http://www.chinanews.com/sh/shipin/', '').replace('http://www.chinanews.com/shipin/', '').replace('.shtml', '').replace('-', '').replace('/', '').replace('news', '')

    else:

        title = sel.xpath('//div[@id="cont_1_1_2"]/h1/text()')

        title = title[0].replace('\r\n      ', '')               #去掉多余换行

        datas = sel.xpath('//div[@ class="left_zw"]/p//text()')
        if '据' in  datas[len(datas) - 1]:
            del[datas[len(datas) - 1]]

        new_datas = ''                                           #将文本列表转换为段落形式
        for data in datas:
            if '记者' in data or '本报实习生' in data or '乐评人' in data:
                pass
            else:
                new_datas = new_datas + data
        new_datas = new_datas.replace('　　', '\n　　')
        save_name = url.replace('http://www.chinanews.com/', '').replace('.shtml', '').replace('-', '').replace('/', '')

    # save_datas = '　　' + title + new_datas                 #组合成需要保存的文本 加空格使标题与正文格式相同

    new_datas = new_datas.replace("（", '(').replace('）', ')')  #括号统一
    new_datas = new_datas.replace('↑', '').replace('■', '').replace('丨', '')

    """正则消除括号内及括号内容"""

    pattern = re.compile('\(.*?\)')
    save_datas = re.sub(pattern, '', new_datas)

    if len(save_datas) < 120:                                #小于120字节不予保存
        print(Thread_name + ':内容过少不予保存' + url)
    else:
        # print(type, save_datas, save_name)
        save_text(type, save_datas, save_name)
        print(Thread_name + ':' + save_name + ':保存成功')


    # print(len(save_datas), type, save_name)
    # print(save_datas)

# Get_detail_page()