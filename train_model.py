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


def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table
def get_crop_imgs(img):
    """
    按照图片的特点,进行切割,这个要根据具体的验证码来进行工作. # 见原理图
    :param img:
    :return:
    """
    child_img_list = []
    for i in range(4):
        x = 2 + i * (8 + 5)  # 见原理图
        y = 0
        child_img = img.crop((x, y, x + 8, y + 18))
        child_img_list.append(child_img)
    return child_img_list

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

# 得到特征值文件
def get_fea_file(img_path,n,flag_print):
    # 遍历图片文件
    for i in os.walk(img_path + '/' + str(n)):
        im_list = i[2]
    for im_file in im_list:
        im_name = './' + img_path + '/' + str(n) + '/' + im_file
        # print(im_name)
        im = Image.open(im_name)
        #  特征选择
        im_feature = get_feature(im)
        # print(im_feature)
        z_index = 1
        if os.path.exists(str(n) + '_feature.txt'):
            ctreate_file = False
        else:
            ctreate_file = True
        # f = open(str(n) + '_feature.txt', 'a')
        # f = open(str(n) + '_feature.txt', 'a')
        #单个特征值文件
        f = open('feature.txt', 'a')
        if ctreate_file:
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

def train_svm_model():
    """
    训练并生成model文件
    :return:
    """
    y, x = svm_read_problem(svm_root + '/train_pix_feature_xy.txt')
    model = svm_train(y, x)
    svm_save_model(model_path, model)

# 将数字全部生成模型
def train_model_main1(n, img_path):
    # 是否打印特征值
    flag_print = True
    # flag_print = False
    # 保存特征值文件
    get_fea_file(img_path, n, flag_print)
def train_model_main2():
    # LibSVM
    # 按照 libSVM 指定的格式生成一组带特征值和标记值的向量文件
    svm_path = r"C:\Python36\risk_down\libsvm"
    sys.path.append(svm_path + r"\python")
    import svmutil
    # y, x = svmutil.svm_read_problem('./' + str(n) + '_feature.txt')
    y, x = svmutil.svm_read_problem('./' + 'feature.txt')
    model = svmutil.svm_train(y[:50], x[:50], '-c 4')
    model_path = "num_feature.model"
    svmutil.svm_save_model(model_path, model)
    # p_label,p_acc,p_val = svmutil.svm_predict(y[0:], x[0:],model)
    # print(p_label,p_acc,p_val)

# 得到测试的特征值文件
def get_fea_file(img_path,n,flag_print):
    # 遍历图片文件
    for i in os.walk(img_path):
        im_list = i[2]
    for im_file in im_list:
        im_name = './' + img_path +  '/' + im_file
        # print(im_name)
        im = Image.open(im_name)
        #  特征选择
        im_feature = get_feature(im)
        # print(im_feature)
        z_index = 1
        f = open(str(n) + '_feature.txt', 'a')
        #单个特征值文件
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

def svm_model_test(svm_root,model_path):
    """
    使用测试集测试模型
    :return:
    """
    svm_path = r"C:\Python36\risk_down\libsvm"
    sys.path.append(svm_path + r"\python")
    import svmutil
    yt, xt = svmutil.svm_read_problem(svm_root + 'last_test_pix_xy_new.txt')
    model = svmutil.svm_load_model(model_path)
    p_label, p_acc, p_val = svmutil.svm_predict(yt, xt, model)#p_label即为识别的结果

    cnt = 0
    for item in p_label:
        print('%d' % item, end=',')
        cnt += 1
        if cnt % 8 == 0:
            print('')

def main():
    img_path = "model_img"
    dir_check(img_path)
    # 图片数字
    n = 0
    for n in range(0,10):
        # train_model_main1(n, img_path)
        # 已经提取特征值
        pass
    # train_model_main2()
    # 到达第二阶段 模型测试
    # get_fea_file('test_pic',8,True)
    svm_model_test('./', "num_feature.model")

if __name__ == '__main__':
    main()