#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Risk2S'''
'''
字符型图片验证码识别完整过程及Python实现
https://www.cnblogs.com/beer/p/5672678.html
'''
import os
from PIL import Image
import numpy as np
import sys


def dir_check(path):
	isExists = os.path.exists(path)
	if isExists != True:
		os.makedirs(path)
		print('文件夹' + path + ' 创建成功')
	else:
		pass

def get_feature(img):
	"""
	获取指定图片的特征值,
	1. 按照每排的像素点,高度为18,则有18个维度,然后为8列,总共144个维度
	:param img_path:
	:return:一个维度为18（高度）的列表
	"""
	width, height = img.size

	pixel_cnt_list = []
	height = 10
	for y in range(height):
		pix_cnt_x = 0
		for x in range(width):
			#  == 0 如果按照示例程序无法提取特征值，如果没有出现，就看看当前像素点的值进行自我处理。
			if img.getpixel((x, y)) < 240:  # 黑色点
				pix_cnt_x += 1

		pixel_cnt_list.append(pix_cnt_x)

	for x in range(width):
		pix_cnt_y = 0
		for y in range(height):
			if img.getpixel((x, y)) < 240:  # 黑色点
				pix_cnt_y += 1

		pixel_cnt_list.append(pix_cnt_y)

	return pixel_cnt_list


# 将数字全部生成模型
def train_model_main1(n, img_path, model_path, flag_print=True):
	# 保存特征值文件
	ff = get_fea_file(img_path, n, flag_print, model_path)
	return ff

def train_model_main2(model_path,file):
	# LibSVM
	# 按照 libSVM 指定的格式生成一组带特征值和标记值的向量文件
	svm_path = r"C:\Python36\risk_down\libsvm"
	sys.path.append(svm_path + r"\python")
	import svmutil
	# y, x = svmutil.svm_read_problem('./' + str(n) + '_feature.txt')
	y, x = svmutil.svm_read_problem(file)
	# ---------------------------------------------------
	model = svmutil.svm_train(y[:50], x[:50], '-c 4')
	# print(model_path,file.split('/')[2][0])
	model_path = './'+model_path+'/'+file.split('/')[2][0]+"_feature.model"
	svmutil.svm_save_model(model_path, model)
	# p_label,p_acc,p_val = svmutil.svm_predict(y[0:], x[0:],model)
	# print(p_label,p_acc,p_val)


# 得到测试的特征值文件
def get_fea_file(img_path, n, flag_print, model_path):
	# 遍历图片文件
	for i in os.walk(img_path + '/' + str(n)):
		img_path = i[0]
		im_list = i[2]
	for im_file in im_list:
		# 文件名，路径
		im_name = './' + img_path + '/' + im_file
		# print(im_name)
		im = Image.open(im_name)
		#  特征选择
		im_feature = get_feature(im)
		# print(im_feature)
		z_index = 1
		feature_name = './' + model_path + '/' + str(n) + '_feature.txt'
		f = open(feature_name, 'a')
		# 单个特征值文件
		# f = open('feature.txt', 'a')
		if flag_print:
			for z in im_feature:
				if z_index == 1:
					print(n, end=' ')
					f.write(str(n) + ' ')
				print(str(z_index) + ':' + str(z), end=' ')
				f.write(str(z_index) + ':' + str(z) + ' ')
				z_index += 1
			print('')
			f.write('\n')
		else:
			for z in im_feature:
				if z_index == 1:
					f.write(str(n) + ' ')
				f.write(str(z_index) + ':' + str(z) + ' ')
				z_index += 1
			f.write('\n')
	f.close()
	return feature_name



def main():
	img_path = "model_img"
	model_path = "model_file"
	dir_check(img_path)
	# 是否打印特征值
	# flag_print = True
	flag_print = False
	get_num = []
	str = input("请输入提取特征值数值，用空格隔开:")
	get_num = str.split(" ")  # lst1用来存储输入的字符串，用空格分割
	# 图片数字
	FNL = []
	for n in get_num:
		if n in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
			fff = train_model_main1(n, img_path, model_path,flag_print)
			FNL.append(fff)
			print(n,"特征值提取成功！")
		else:
			print("提取错误")
			continue
	# n = 0
	# train_model_main1(n, img_path, model_path,flag_print)
	# for n in range(0,10):
	#     train_model_main1(n, img_path, model_path)
	#     # 已经提取特征值
	#     pass
	# FNL 特征值文本文件名，路径
	for file in FNL[0:]:
		train_model_main2(model_path,file)


if __name__ == '__main__':
	main()
