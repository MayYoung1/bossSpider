import json
import random
from scrapydemo.boss.models import ProxyModel
import requests
from twisted.internet.defer import DeferredLock

class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
        'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+',
        'Opera/9.80 (Android; Opera Mini/36.2.2254/119.132; U; id) Presto/2.12.423 Version/12.16',
        'iTunes/9.1.1',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
        'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
        'Mozilla/5.0 (X11; U; UNICOS lcLinux; en-US) Gecko/20140730 (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
    ]

    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent

class IPProxyDownloadMiddleware(object):
    PROXY_URL = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='

    def __init__(self):
        super(IPProxyDownloadMiddleware,self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()


    def process_request(self,request,spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            self.update_proxy()

        request.meta['proxy'] = self.current_proxy.proxy


    def process_response(self,request,response,spider):
        if response.status != 200 or "captcha" in response.url :
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            print('%s这个代理被加入黑名单'%self.current_proxy.ip)
            self.update_proxy()
            return request
        return response

    def update_proxy(self):
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            print('重新获取一个代理', text)
            result = json.loads(text)
            if len(result['data']) > 0:
                data = result['data'][0]
                proxy_modle = ProxyModel(data)
                self.current_proxy = proxy_modle
        self.lock.release()