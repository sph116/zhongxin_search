import os

paths = ['科教文卫', '时政新闻', '国际新闻', '财经新闻', '娱乐新闻', '港澳台海外华人新闻', '社会新闻', '城建公交', '体育新闻', '军事新闻']      #所有路径
"""用于创建文件路径"""
try:
    for path in paths:
        os.mkdir('./' + path)
    print('文件保存路径创建成功')
except Exception as e:
    print(e)


def save_text(type, save_datas, save_name):

    """
    新闻类型分类分类及保存
    :param type:
    :param save_datas:
    :param save_name:
    :return:
    """

    # paths = ['科教文卫', '时政新闻', '国际新闻', '财经新闻', '娱乐新闻', '港澳台海外华人新闻', '社会新闻', '城建公交', '体育新闻', '军事新闻']      #所有路径
    """用于创建文件路径"""
    # try:
    #     for path in paths:
    #         os.mkdir('C:/Users/孙佩豪/Desktop/爬虫（工作）/中国新闻网滚动页面/文档未处理/' + path)
    #         print('创建成功')
    # except Exception as e:
    #     print(e)

    if type == 'IT频道' or type == '教育频道 ' or type == '海外华文报摘' or type == '能源频道' or type == '文化新闻':
        type = '科教文卫'
    elif type == '国内新闻':
        type = '时政新闻'
    elif type == '国际新闻':
        type = '国际新闻'
    elif type == '财经频道' or type == '金融频道' or type == '证券频道' or type == '产经中心':
        type = '财经新闻'
    elif type == '娱乐新闻':
        type = '娱乐新闻'
    elif type == '港澳新闻' or type == '台湾新闻' or type == '华人新闻':
        type = '港澳台海外华人新闻'
    elif type == '社会新闻' or type == '地方频道' or type == '图片新闻' or type == '地方频道' or type == '视频新闻' or type == '汽车频道' or type == '健康频道' or type == '葡萄酒频道':
        type = '社会新闻'
    elif type == '房产频道' or type == '生活频道':
        type = '城建公交'
    elif type == '体育新闻':
        type = '体育新闻'
    elif type == '军事新闻':
        type = '军事新闻'

    with open('./' + type + '/' + save_name + '.txt', 'w+', encoding='utf-8') as g:
        g.write('\n' + str(save_datas))
        g.close()
        # print('线程 ：' + self.name + '：文本' + save_name, ' 保存完成')














