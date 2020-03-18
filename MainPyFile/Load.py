import sys
import time
from gensim.models import Word2Vec
import logging

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    print('主程序开始执行...')
    sTime = time.time()
    print('开始时间：' + time.ctime())

    file = open('wordsim-240.txt', mode='r', encoding='utf-8')
    model = Word2Vec.load('wiki.model')
    print('模型与测试集加载完成')

    _sTime = time.time()
    for s in file.readlines():
        list = s.split()
        s1 = list[0]
        s2 = list[1]
        try:
            print(model.wv.similarity(s1, s2))
        except Exception as e:
            print(e)
    _eTime = time.time()
    print('WordSim-240相似度比较耗时：' + str(int((_eTime - _sTime) * 1000)) + 'ms')
    print('主程序执行结束！')
    eTime = time.time()
    print('结束时间：' + time.ctime())
    print('总时间耗时：' + str(int(eTime - sTime)) + 's')
