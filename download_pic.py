#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Risk2S'''
import requests
import os
codeurl = "http://jwc.sicnu.edu.cn/admin/Validate.aspx"
# 参数初始值
username = 'admin'
password = 'root'
code = '0000'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
           "Content-Type": "application/x-www-form-urlencoded",
           "Referer": "http://jwc.sicnu.edu.cn/admin/login.aspx"}

cookies = {
	'Cookie':'ASP.NET_SessionId=y5wjx4h2zla02z3b3gngvong'
}

post_data = {
	'__VIEWSTATE':"/wEPDwUJOTM1NzIxMTI5D2QWAgIDD2QWAgIBDw8WAh4EVGV4dAUiKiog5o+Q56S66ZSZ6K+v77ya6aqM6K+B56CB6ZSZ6K+vIWRkZGmEyfVSizCFlUzWmpq0MvZusXA0P71fXn2Biz0JeWs6",'__EVENTVALIDATION':"82312306",
	'__EVENTVALIDATION':"/wEdAAXlVHPNsMM+vvvlEp/0HzeRDFTzKcXJqLg+OeJ6QAEa2nY2+Mc6SrnAqio3oCKbxYZyS2f5c1XgBSx3nGmY/9ewPOaW1pQztoQA36D1w/+bXeDqyuyA551HX4tXs+8SOVWmkog+AGYh7ylorI7F9Y/E",
	'txtUser':'admin','txtPassword':'admin',
	'txtValidate':code,'btnSubmit':" 登 录 ",
}

# 验证码下载
def get_pic(s ,pic_name):
    global codeurl
    path = 'images'
    isExists=os.path.exists(path)
    if isExists != True:
        os.makedirs(path)
        print('文件夹'+path+' 创建成功')
    else:
        pass
    # 得到验证码图片
    rcode = s.get(codeurl)
    f = open('./images/{}.png'.format(pic_name), 'wb')
    f.write(rcode.content)
    f.close()
    print(pic_name,"\t图片写入成功！")


def main():
    # 利用session 保持同步
    s = requests.Session()
    # 图片数量
    end_num = 100
    for i in range(0,end_num):
        pic_name = 'pic_'+str(i)
        get_pic(s, pic_name)

if __name__ == '__main__':
    main()