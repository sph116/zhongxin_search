import threading
import time
from queue import Queue
from get_detail_page import Get_detail_page
from ip_pool import ip_pool
from mysql_module import mysql
from ip_pool import ip_flag
from get_url_list import Get_url_list
import ctypes
time.sleep(2)

url_queue = Queue()       #构造一个不限大小的队列
threads = []             #构造工作线程池
flag = 0  #维护线程 是否停止的标志位


class Spider(threading.Thread):
    """多线程类"""
    def __init__(self, Thread_name, func):
        super().__init__()
        self.Thread_name = Thread_name
        self.func = func

    def run(self):
        self.func(self.name)

def worker(Thread_name):

    """
    工作方法
    :param Thread_name:
    :return:
    """
    global url_queue
    print(Thread_name + ':启动')
    while not url_queue.empty():   #队列不为空继续运行
        url = url_queue.get()
        url1 = 'http://www.chinanews.com' + url.replace('http://www.chinanews.com', '')
        Get_detail_page(url1, Thread_name)

def thread_manage(THREAD_NAME):
    """
    保护线程方法 线程挂了再次构建线程
    :param THREAD_NAME:
    :return:
    """
    global flag
    print(THREAD_NAME + ":启动")
    while 1:
        if flag == 1:
            print("维护线程池结束。")
            break
        for thread in threads:
            # print(thread.isAlive())
            if not thread.isAlive():   #判断线程是否存在
                threads.remove(thread)
                thread = Spider(thread.getName(), worker)
                print("已恢复线程"+thread.getName())
                threads.append(thread)
                thread.start()
        time.sleep(60)

def main():
    """
    主线程
    :return:
    """
    global url_queue
    global flag


    start = time.time()
    threadNum = 5    # 线程数量
    param = 6711960   #页面规则 6711960项数据 0+100 翻页
    # k = 0            # 爬取数初始


    """为ip池构造线程"""
    t = threading.Thread(target=ip_pool, args=('Thread_IP',))
    t.setDaemon(True)
    t.start()

    """为守护线程构造线程"""
    f = threading.Thread(target=thread_manage, args=('Thread_manager',))
    # t.setDaemon(True)
    f.start()


    """为详情页url构造线程"""
    f = threading.Thread(target=Get_url_list, args=(param, 'Thread_get_url',))
    f.start()
    # time.sleep(100)

    while True:
        if url_queue.qsize() <= 1000:
            """若队列长度小于1000 继续获取url列表"""
            url_list = mysql.get_data()
            if len(url_list) < 100:
                print('Thread_main:爬取完毕 爬虫结束')
                ip_flag(flag)
                flag = 1
                break
            wrong_urls = mysql.get_wrong_data()  # 获取需要重新爬取url列表
            url_list = url_list + wrong_urls
            print('Thread_main:url队列剩余数量' + str(len(url_list)))
            for i in range(0, len(url_list) - 1):
                url_queue.put(url_list[i])
            print('Thread_main:url队列更新成功')

        else:
            pass

        if len(threads) == 0:

            """构造采集线程"""
            for i in range(1, threadNum+1):
                thread = Spider("Thread_" + str(i), worker)
                thread.start()
                threads.append(thread)

            """阻塞"""
            for thread in threads:
                thread.join()

        else:
            pass
        time.sleep(300)

    end = time.time()
    print("-------------------------------")
    print("下载完成. 用时{}秒".format(end - start))

if __name__ == "__main__":
    main()

