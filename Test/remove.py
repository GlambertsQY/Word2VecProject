# coding:utf-8
import re

if __name__ == '__main__':
    print('主程序执行开始...')

    input_file_name = 'problemData.separate.txt'
    output_file_name = 'problemData_out.txt'
    input_file = open(input_file_name, 'r', encoding='utf-8')
    output_file = open(output_file_name, 'w', encoding='utf-8')

    print('开始读入数据文件...')
    lines = input_file.readlines()
    print('读入数据文件结束！')

    print('分词程序执行开始...')
    count = 1
    cn_reg = '^[\u4e00-\u9fa5]+$'

    for line in lines:
        # line_list = line.split('\n')[0].split(' ')
        line_list = str(line.split('\n')[0].split(' '))
        line_list_new = []
        for word in line_list:
            if re.search(cn_reg, word):
                line_list_new.append(word)
        print(line_list_new)
        # output_file.write(' '.join(line_list_new) + '\n')
        for i in line_list_new:
            output_file.write(i)
        output_file.write('\n')

        count += 1
        if count % 10000 == 0:
            print('目前已分词%d条数据' % count)
    print('分词程序执行结束！')
    input_file.close()
    output_file.close()
    print('主程序执行结束！')
