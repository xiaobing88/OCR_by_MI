#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Risk2S'''
import os
from PIL import Image
import numpy as np

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
    :return:table
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

def main():
    dir_check('tmp')
    img_path = "images"
    n = 0
    # 遍历图片文件
    for i in os.walk(img_path):
        im_list = i[2]
    for im_file in im_list:
        im_name = './'+img_path+'/'+im_file
        im = Image.open(im_name)
        # 二值化图片 将RGB彩图转为灰度图
        im_grey = im.convert('L')
        # im_grey.show()
        # 灰度图按照设定阈值转化为二值图
        # if_bin_img = True
        if_bin_img = False
        if if_bin_img:
            table = get_bin_table(200)
            out = im_grey.point(table, '1')
        else:
            out = im_grey
        #   分割图片
        images = get_crop_imgs(out)
        for i in images:
            o = i.resize((8, 18))
            o.save('./tmp/'+str(n)+'.png','PNG')
            n += 1

if __name__ == '__main__':
    main()