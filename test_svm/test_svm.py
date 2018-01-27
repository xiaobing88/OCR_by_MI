#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''Risk2S'''
import os
from PIL import Image
import numpy as np
import sys
# 将libsvm包放入\Lib\site-packages目录下
from libsvm.python.svmutil import *
from libsvm.python.svm import *
# svmutil.py, line 5,
# 5、6 行的from svm import *改为from .svm import *


def main():
    y, x = svm_read_problem('train.txt')
    yt, xt = svm_read_problem('test.txt')
    # 训练模型过程中，参数含义
    """
    iter 为迭代次数，
    nu  与前面的操作参数 -n nu  相同，
    obj 为 SVM 文件转换为的二次规划求解得到的最小值，
    rho  为判决函数的常数项 b ，
    nSV  为支持向量个数，
    nBSV 为边界上的支持向量个数，
    Total nSV 为支持向量总个数
    """
    model = svm_train(y, x)
    print('测试结果:',end='\t')
    p_label, p_acc, p_val = svm_predict(yt, xt, model)
    print(p_label)

if __name__ == '__main__':
    main()