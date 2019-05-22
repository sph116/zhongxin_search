
import requests
import time


using_ips = []

def ip_pool(thread_name):

    global using_ips
    global ip_flag

    print(thread_name + ':启动')

    while 1:
        if ip_flag == 1:
            print(thread_name + "线程结束。")
            break
        print(thread_name + ':当前代理池ip数量' + str(len(using_ips)) + '----------------')
        if len(using_ips) < 5:
            try:

                api_url = "http://dev.kdlapi.com/api/getproxy/?orderid=974511275220126&num=20&area=%E5%9B%BD%E5%86%85&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sep=%E3%80%82"
                rep = requests.get(api_url, timeout=5)
                ips = rep.text.split('。')
                for ip in ips:
                    using_ips.append(ip)

            except:
                continue
        else:
            pass
        time.sleep(30)

def ip_flag(flag):
    global ip_flag
    ip_flag = flag


def get_ip():
    global using_ips
    while len(using_ips) == 0:
        pass
    a = using_ips.pop(0)
    return a

