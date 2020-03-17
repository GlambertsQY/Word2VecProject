import time
import threading
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import gensim.models
import multiprocessing
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    input_file_name = 'problemData.out.txt'
    model_file_name = 'wiki_new.model'

    print('主程序开始执行...')
    sTime = time.time()
    print('开始时间：' + time.ctime())

    model = gensim.models.Word2Vec.load(model_file_name)
    print('加载完成..')

    model.build_vocab(LineSentence(input_file_name), update=True)
    print('开始训练..')
    model.train(LineSentence(input_file_name), total_examples=model.corpus_count, epochs=model.iter)
    model.save('wiki_new.model')

    print('主程序执行结束！')
    eTime = time.time()
    print('结束时间：' + time.ctime())
    print('总时间耗时：' + str(int(eTime - sTime)) + 's')
