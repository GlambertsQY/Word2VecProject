from gensim.models import Word2Vec
import jieba
import jieba.posseg as jp
import numpy as np
from scipy.linalg import norm
import time

model_file = 'wiki_new.model'
model = Word2Vec.load(model_file)

flagList = ['n', 'v', 'a', 'd']
sims = [0] * 4
lam = 0
s_len = [0] * 2
alpha1 = 0.8
alpha2 = 0.1
alpha3 = 0.05
alpha4 = 0.05


def sentenceSimilarity(s1, s2):
    def sentence2Vec(s, n):
        line_cut = jp.cut(s)
        l = []
        dic = {}
        for key in line_cut:
            if key.flag[0] in flagList:
                dic[key.word] = key.flag[0]
                l.append(key.word)
        s_len[n] = len(l)
        v = [np.zeros(64)] * 4
        v_n = [0] * 4
        for key, value in dic.items():
            if value == 'n':
                try:
                    v[0] = v[0] + model[key]
                    v_n[0] = v_n[0] + 1
                except Exception as e:
                    print(e)
            elif value == 'v':
                try:
                    v[1] = v[1] + model[key]
                    v_n[1] = v_n[1] + 1
                except Exception as e:
                    print(e)
            elif value == 'a':
                try:
                    v[2] = v[2] + model[key]
                    v_n[2] = v_n[2] + 1
                except Exception as e:
                    print(e)
            elif value == 'd':
                try:
                    v[3] = v[3] + model[key]
                    v_n[3] = v_n[3] + 1
                except Exception as e:
                    print(e)
            else:
                print('出错')
        for i in range(0, 4):
            if v_n[i] != 0:
                v[i] /= v_n[i]
        return v

    v1, v2 = sentence2Vec(s1, 0), sentence2Vec(s2, 1)
    lam = 2 * min(s_len[0], s_len[1]) / (s_len[0] + s_len[1])
    for i in range(0, 4):
        if any(v1[i]) and any(v2[i]):
            sims[i] = np.dot(v1[i], v2[i]) / (norm(v1[i]) * norm(v2[i]))
    return lam * (alpha1 * sims[0] + alpha2 * sims[1] + alpha3 * sims[2] + alpha4 * sims[3])


def sent_most_similarity(s1, s2):
    def sentence2List(s):
        line_cut = jp.cut(s)
        l = []
        for key in line_cut:
            if key.flag[0] == 'n':
                l.append(key.word)
        return l

    dic_s = {}
    l1, l2 = sentence2List(s1), sentence2List(s2)
    for i in l1:
        for j in l2:
            try:
                dic_s[model.wv.similarity(i, j)] = i + ' ' + j
            except Exception as e:
                print(e)
    dic_s = sorted(dic_s.items(), key=lambda x: x[0], reverse=True)
    return dic_s


if __name__ == '__main__':
    input_file_name = 'problemData.txt'
    input_file = open(input_file_name, mode='r', encoding='utf-8')
    str_list = []
    str_list = input_file.read().split('\\')
    l1 = []
    l2 = []
    l3 = []
    for i in str_list:
        i = i.strip()
        try:
            if i != '':
                if i[0].isdigit():
                    t = i.split('&')
                    l1.append(t[0].split('\t')[1].strip())
                    t[1] = t[1].strip().strip('答：')
                    l2.append(t[1].strip())
                    t[2] = t[2].strip().strip('错答：')
                    l3.append(t[2].strip())
        except Exception as e:
            print(i)

    s1 = []
    s2 = []
    s1_s2 = []
    sTime = time.time()
    for i in range(0, len(l2)):
        s1.append(sentenceSimilarity(l2[i], l2[i]))
        s2.append(sentenceSimilarity(l2[i], l3[i]))
        s1_s2.append(s1[i] - s2[i])
    eTime = time.time()
    sum = 0

    o1 = []
    o2 = []
    for i in range(0, len(s1_s2)):
        if s1_s2[i] >= 0.5:
            sum = sum + 1
    print('耗时：' + str(int((eTime - sTime) * 1000)) + 'ms')
    print('符合个数：' + str(sum))
    print('End')
