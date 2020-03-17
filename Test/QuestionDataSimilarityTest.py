from gensim.models import Word2Vec

model_file = 'wiki_new.model'
model = Word2Vec.load(model_file)

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

    print('End')
