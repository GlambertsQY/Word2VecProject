from gensim.models import Word2Vec
import jieba.posseg as jp
import numpy as np
from scipy.linalg import norm

model_file = 'test.model'
model = Word2Vec.load(model_file)
flagList = ['n', 'v', 'a', 'd']


def test(s: str):
    l = jp.cut(s)
    t = []
    for key in l:
        # 去除停用词
        # print(key.word + ' ' + key.flag)
        if key.flag[0] in flagList:
            t.append(key.word)
    print(t)


def readFile(s):
    input_file = open(s, mode='r', encoding='utf-8')
    lines = input_file.readlines()
    for line in lines:
        test(line)


def sent_Similarity(s1, s2):
    line_cut1 = jp.cut(s1)
    line_cut2 = jp.cut(s2)
    l1 = []
    l2 = []
    dict1 = {}
    dict2 = {}
    for key in line_cut1:
        if key.flag[0] in flagList:
            dict1[key.word] = key.flag[0]
            l1.append(key.word)
    for key in line_cut2:
        if key.flag[0] in flagList:
            dict2[key.word] = key.flag[0]
            l2.append(key.word)

    vn1, vv1, va1, vd1 = np.zeros(64), np.zeros(64), np.zeros(64), np.zeros(64)
    vn1_n, vv1_n, va1_n, vd1_n = 0, 0, 0, 0
    for k, v in dict1.items():
        if v == 'n':
            vn1 += model[k]
            vn1_n += 1
        elif v == 'v':
            vv1 += model[k]
            vv1_n += 1
        elif v == 'a':
            va1 += model[k]
            va1_n += 1
        elif v == 'd':
            vd1 += model[k]
            vd1_n += 1
        else:
            print('出错')
    if vn1_n != 0:
        vn1 /= vn1_n
    if vv1_n != 0:
        vv1 /= vv1_n
    if va1_n != 0:
        va1 /= va1_n
    if vd1_n != 0:
        vd1 /= vd1_n

    vn2, vv2, va2, vd2 = np.zeros(64), np.zeros(64), np.zeros(64), np.zeros(64)
    vn2_n, vv2_n, va2_n, vd2_n = 0, 0, 0, 0
    for k, v in dict2.items():
        if v == 'n':
            vn2 += model[k]
            vn2_n += 1
        elif v == 'v':
            vv2 += model[k]
            vv2_n += 1
        elif v == 'a':
            va2 += model[k]
            va2_n += 1
        elif v == 'd':
            vd2 += model[k]
            vd2_n += 1
        else:
            print('出错')
    if vn2_n != 0:
        vn2 /= vn2_n
    if vv2_n != 0:
        vv2 /= vv2_n
    if va2_n != 0:
        va2 /= va2_n
    if vd2_n != 0:
        vd2 /= vd2_n

    sim1, sim2, sim3, sim4 = 0, 0, 0, 0
    lam = 2 * min(len(l1), len(l2)) / (len(l1) + len(l2))
    if any(vn1) and any(vn2):
        sim1 = np.dot(vn1, vn2) / (norm(vn1) * norm(vn2))
    if any(vv1) and any(vv2):
        sim2 = np.dot(vv1, vv2) / (norm(vv1) * norm(vv2))
    if any(va1) and any(va2):
        sim3 = np.dot(va1, va2) / (norm(va1) * norm(va2))
    if any(vd1) and any(vd2):
        sim4 = np.dot(vd1, vd2) / (norm(vd1) * norm(vd2))
    alpha1 = 0.8
    alpha2 = 0.1
    alpha3 = 0.05
    alpha4 = 0.05
    return lam * (alpha1 * sim1 + alpha2 * sim2 + alpha3 * sim3 + alpha4 * sim4)


if __name__ == '__main__':
    myDict = {'s': 'w', 'a': 'e'}
    t = []
    s1 = '指令是计算机完成一个功能的最小操作，它由操作码和地址码组成，过程是取指令、分析指令和执行指令。'
    s2 = '指令是计算机完成一个功能的操作，它由操作码和地址码组成，过程是取指令、分析指令和执行指令。'

    l = [np.zeros(64)] * 4
    l[0] = l[0] + model['指令']
    print('End')
