# OCR_by_MI
![Python Version](https://img.shields.io/badge/python-3.6-blue.svg)

# 基于向量机算法的数字识别
<p align="center"><img src="https://i.imgur.com/uL3Z3Jl.jpg" /></p>

## 前言
验证码识别涉及很多方面的内容。入手难度大,但是入手后,可拓展性又非常广泛,可玩性极强,成就感也很足。

验证码内的字符识别主要以机器学习的分类算法来完成,目前我所利用的字符识别的算法为KNN(K邻近算法)和SVM (支持向量机算法)

本文使用SVM，适合初学者，简单易懂，效果显著

## 关键词
OCR_by_MI
验证码识别 机器学习 SVM (支持向量机算法)

##大致流程
- 抓取原始图片素材（验证码图片）
- 原始图片处理 （灰度化）
- 图片切割 （图片切割成单个字符的小图片）
- 图片尺寸归一化 （小图片变为同种格式）
- 图片字符标记 （人工分类小图片，并打标）
- 图片特征提取
- 得到特定格式的特征训练集
- 通过模型实现图片验证码
## 使用方法
```python
python runserver.py
```

## 参考资料
[教务处引起的验证码识别的机器学习-Python版本][https://xiaobing88.github.io/2018/01/27/%E6%95%99%E5%8A%A1%E5%A4%84%E5%BC%95%E8%B5%B7%E7%9A%84%E9%AA%8C%E8%AF%81%E7%A0%81%E8%AF%86%E5%88%AB%E7%9A%84%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0-Python%E7%89%88%E6%9C%AC/]
