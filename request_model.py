import requests
import random
from ip_pool import get_ip
from lxml import etree
# from fake_useragent import UserAgent




class download():

    def __init__(self):
        # ua = UserAgent()           #UA实例化 链接网络不稳定

        self.UA = []
        self.UA.append('Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')
        self.UA.append('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0')
        self.UA.append('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)')



    def get(self, url, timeout, proxy=None, num_retries=0, ip_times=6):

        headers = {'User-Agent': random.choice(self.UA)}      #随机ua

        if proxy == None:                   #当代理为空时，不使用代理获取response
            try:
                rep = requests.get(url=url, headers=headers, timeout=timeout)

                if rep.status_code == 200:
                    return(rep)
                else:
                    raise NameError



            except Exception as e:              #如过上面的代码执行报错则执行下面代码
                # print(e)

                if num_retries > 0:             #num_retries是我们限定的重试次数

                    return self.get(url, timeout, num_retries=num_retries-1)

                else:
                    """获取代理"""
                    a = get_ip()
                    ip1 = "http://" + a
                    proxy = {'http': ip1}

                    return self.get(url, timeout, proxy)
        else:
            try:
                # print(proxy)
                # print('get raw正在启用代理： ', proxy)
                rep = requests.get(url=url, headers=headers, timeout=timeout, proxies=proxy)
                if rep.status_code == 200:
                    return rep
                else:
                    raise NameError
                # else:
                #     raise NameError

            except Exception as e:
                print(e)

                if ip_times > 0:
                    # print('代理爬取失败，重试第', ip_times, '次')
                    a = get_ip()
                    ip2 = "http://" + a
                    proxy = {'http': ip2}
                    return self.get(url, timeout, proxy, ip_times=ip_times - 1)

                else:
                    return requests.get(url=url, headers=headers, timeout=timeout)



class download1():

    def __init__(self):
        # ua = UserAgent()           #UA实例化 链接网络不稳定

        self.UA = []
        self.UA.append('Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')
        self.UA.append('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0')
        self.UA.append('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)')

    def get(self, url, data, timeout, proxy=None, num_retries=0, ip_times=10):

        headers = {'User-Agent': random.choice(self.UA)}      #随机ua

        if proxy == None:                   #当代理为空时，不使用代理获取response
            try:
                rep = requests.post(url=url, data=data, headers=headers, timeout=timeout)
                if rep.status_code == 200:
                    rep.encoding = rep.apparent_encoding
                    sel = etree.HTML(rep.text)
                    if sel.xpath('//div[@id="news_list"]/table//tr[1]/td[2]/ul/li[1]/a/@href') == []:
                        raise NameError
                    else:
                        return rep
                else:
                    raise NameError



            except Exception as e:              #如过上面的代码执行报错则执行下面代码
                # print(e)
                if num_retries > 0:             #num_retries是我们限定的重试次数
                    return self.get(url, timeout, num_retries=num_retries-1)

                else:
                    """获取代理"""
                    a = get_ip()
                    ip1 = "http://" + a
                    proxy = {'http': ip1}
                    return self.get(url, timeout, data, proxy)
        else:
            try:
                # print(proxy)
                print('get raw正在启用代理： ', proxy)
                rep = requests.post(url=url, data=data, headers=headers, timeout=timeout, proxies=proxy)
                if rep.status_code == 200:
                    rep.encoding = rep.apparent_encoding  # 解决编码问题
                    sel = etree.HTML(rep.text)
                    if sel.xpath('//div[@id="news_list"]/table//tr[1]/td[2]/ul/li[1]/a/@href') == []:
                        raise NameError
                    else:
                        return rep
                else:
                    raise NameError
                # else:
                #     raise NameError

            except Exception as e:
                # print(e)
                if ip_times > 0:
                    # print('代理爬取失败，重试第', ip_times, '次')
                    a = get_ip()
                    ip2 = "http://" + a
                    proxy = {'http': ip2}
                    return self.get(url, timeout, data, proxy, ip_times=ip_times - 1)

                else:

                    return requests.post(url=url, headers=headers, data=data, timeout=timeout)

request = download()
request1 = download1()
