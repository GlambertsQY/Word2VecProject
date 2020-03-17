# coding:utf-8
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import time
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == "__main__":
    print('主程序开始执行...')
    sTime = time.time()
    print('开始时间：' + time.ctime())

    input_file_name = 'wiki.txt'
    model_file_name = 'wiki_new.model'

    print('转换过程开始...')
    model = Word2Vec(LineSentence(input_file_name),
                     size=64,  # 词向量长度为64
                     window=5,
                     min_count=1,  # 词出现数低于此将被忽略
                     workers=multiprocessing.cpu_count())
    print('转换过程结束！')

    print('开始保存模型...')
    model.save(model_file_name)
    print('模型保存结束！')

    print('主程序执行结束！')
    eTime = time.time()
    print('结束时间：' + time.ctime())
    print('耗时：' + str(int(eTime - sTime)) + '秒')
