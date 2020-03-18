# from gensim.models import Word2Vec
import time
import MainPyFile.SentenceSimilarity
from sqlalchemy import String, Column, Integer, Text, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# model_file = 'wiki_new.model'
# model = Word2Vec.load(model_file)
engine = create_engine('mysql+pymysql://root:Abc123456@106.14.141.128/graduationproject?charset=utf8')
session = sessionmaker(bind=engine)
Base = declarative_base()


class Question(Base):  # 必须继承declaraive_base得到的那个基类
    __tablename__ = "question"  # 必须要有__tablename__来指出这个类对应什么表，这个表可以暂时在库中不存在，SQLAlchemy会帮我们创建这个表
    id_q = Column(Integer, primary_key=True, autoincrement='auto')  # Column类创建一个字段
    text_q = Column(Text,
                    nullable=False)  # nullable就是决定是否not null，unique就是决定是否unique。。这里假定没人重名，设置index可以让系统自动根据这个字段为基础建立索引
    subject = Column(String(20), nullable=False)

    # standardanswers = relationship('StandardAnswer', backref='questions')

    def __repr__(self):
        return '<Question>{}:{}'.format(self.id_q, self.text)


class StandardAnswer(Base):
    __tablename__ = 'standardanswer'
    id_s = Column(Integer, primary_key=True, autoincrement='auto')
    text_s = Column(Text, nullable=False)
    id_q = Column(Integer, ForeignKey(Question.id_q), nullable=False)

    def __repr__(self):
        return '<StandardAnswer>{}:{}'.format(self.id_s, self.text)


Session = sessionmaker(bind=engine)
session = Session()  # 实例化了一个会话（或叫事务），之后的所有操作都是基于这个对象的

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
        s1.append(MainPyFile.SentenceSimilarity.sentSimilarity(l2[i], l2[i]))
        s2.append(MainPyFile.SentenceSimilarity.sentSimilarity(l2[i], l3[i]))
        s1_s2.append(s1[i] - s2[i])
    eTime = time.time()
    sum = 0

    o1 = []
    o2 = []
    for i in range(0, len(s1_s2)):
        if s1_s2[i] >= 0.5:
            o1.append(l1[i])
            o2.append(l2[i])
            sum = sum + 1

    for i in range(0, len(o1)):
        question = Question(id_q=i + 1, text_q=o1[i], subject='计算机')
        session.add(question)
        session.commit()
    for i in range(0, len(o2)):
        sa = StandardAnswer(id_s=i + 1, text_s=o2[i], id_q=i + 1)
        session.add(sa)
        session.commit()
    session.close()
    print('耗时：' + str(int((eTime - sTime) * 1000)) + 'ms')
    print('符合个数：' + str(sum))
    print('End')
