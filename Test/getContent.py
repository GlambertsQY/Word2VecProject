import gensim
import pandas as pd

if __name__ == "__main__":
    model = gensim.models.Word2Vec.load('word2vec_wx')
    print(model.similarity(u'微信', u'私信'))
