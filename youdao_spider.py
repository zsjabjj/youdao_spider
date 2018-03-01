# -*- coding: utf-8 -*-
import hashlib
import json
import random
import re
import requests
import time


class Youdao(object):
    def __init__(self):
        # 构建url
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

        # 构建请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer': 'http: // fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-1095750627@101.81.193.97; OUTFOX_SEARCH_USER_ID_NCOO=2024303124.095637; JSESSIONID=aaaGhbJ88P_bVgm5lfiew; ___rl__test__cookies=1516259086284'
        }

        # post请求, 构建POST数据
        self.post_data = None

    def create_post_data(self, word):
        '''构建POST请求数据'''
        # r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
        # 构建时间戳
        time_int = time.time()
        time_re = re.match(r'(\d+).(\d+)', str(time_int))
        time_str = time_re.group(1) + time_re.group(2)
        time_stamp = time_str[0:13]

        # 获取随机数
        random_int = random.randint(0, 9)

        # 获得salt值
        salt = str(int(time_stamp) + random_int)

        '''
        o = u.md5(E + n + r + O)

        E = "fanyideskweb"
        n = 要翻译的字符串
        r = salt
        O = "aNPG!!u6sesA>hBAW1@(-"
        '''
        E = "fanyideskweb"
        n = word
        r = salt
        O = "aNPG!!u6sesA>hBAW1@(-"
        md5_str = E + n + r + O

        # 创建hash对象
        md5 = hashlib.md5()

        # 填充数据
        # Update the hash object with the bytes in arg. Repeated calls
        # are equivalent to a single call with the concatenation of all
        # the arguments
        md5.update(md5_str.encode())

        # 获取hash值
        # Return the digest of the bytes passed to the update() method so far
        sign = md5.hexdigest()

        self.post_data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': False,
        }

    def get_data(self):
        '''发送请求, 获取响应'''
        resp = requests.post(self.url, headers=self.headers, data=self.post_data)
        return resp.content.decode()

    def parse_data(self, data):
        '''解析响应, 获取数据'''
        # data是json字符串, 需要转成字典提取数据
        dict_data = json.loads(data)
        result = dict_data['translateResult'][0][0]
        print('翻译前:%s\n翻译后:%s' % (result['src'], result['tgt']))

    def run(self, data):
        # 构建POST数据
        self.create_post_data(data)
        # 发送请求, 获取响应
        resp_data = self.get_data()
        # 分析数据, 打印结果
        self.parse_data(resp_data)


if __name__ == '__main__':
    data = input('请输入需要翻译的内容:')
    youdao = Youdao()
    youdao.run(data)

'''
i:蜘蛛
from:AUTO
to:AUTO
smartresult:dict
client:fanyideskweb
salt:1516259086293
sign:6c6c37c5c0b8b95f23e0785342d8bb2b
doctype:json
version:2.1
keyfrom:fanyi.web
action:FY_BY_CLICKBUTTION
typoResult:false

i: n,
from: _,
to: C,
smartresult: "dict",
client: E,
salt: r,
sign: o,
doctype: "json",
version: "2.1",
keyfrom: "fanyi.web",
action: e || "FY_BY_DEFAULT",
typoResult: !1

如果你用一个字符串加上一个数字（或其他值），那么操作数都会被首先转换为字符串。如下所示：

"3" + 4 + 5; // 345
3 + 4 + "5"; // 75
这里不难看出一个实用的技巧——通过与空字符串相加，可以将某个变量快速转换成字符串类型。

r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
o = u.md5(E + n + r + O)

E = "fanyideskweb"
n = 要翻译的字符串
r = salt
O = "aNPG!!u6sesA>hBAW1@(-"

'''
