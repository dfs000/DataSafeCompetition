# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 14:00
# @Author  : dfs
# @FileName: main.py
# @Team    : qingan
# @Describe:
import os
import csv
import time
from ocr import analysis_ocr_result

def search_sensitive_file(base_path, sensitive_word):
    # =====================step1. 设置结果写入的文件名称以及读取的文件列表=====================#
    # 获取写入的csv文件名称
    csv_path = 'result_' + time.strftime("%Y%m%d-%H:%M:%S") + '.csv'
    with open(csv_path, 'w') as f:
        csv_write = csv.writer(f)
        csv_head = ["文件名称", "文件内所含敏感词", "文件所在路径"]
        csv_write.writerow(csv_head)

    # 获取要分析的文件列表
    file_list = os.listdir(base_path)

    # result存放的是命中的敏感词
    result = []

    # sensitive_file_list存放的是命中的敏感文件列表，这个跟result是一一对应的
    sensitive_file_list = []

    # sensitive_file_path_list存放的是命中的敏感文件路径列表，这个跟result也是一一对应的
    sensitive_file_path_list = []

    # =====================step2. 设置文件类型列表=====================#
    # 图像文件后缀名
    img_type_list = ['.jpg', '.png']
    # 压缩文件后缀名
    compressed_type_list = ['.zip', '.rar', '.7z']
    # 文本文件后缀名
    text_type_list = ['.txt', '.docx', '.pdf']
    # 未知类型，进行统计
    unknown_type_list = []

    # =====================step3. 遍历每一个文件进行分析，找出含有敏感词的文件=====================#
    for file in file_list:

        # 获取文件后缀名，判断类型执行相应的查找方法
        file_type = file[file.rfind('.'):]

        # 拼接文件的路径
        file_path = base_path + '/' + file

        if file_type in img_type_list:
            sensitive_word_string = search_img_file(file_path, sensitive_word)
            if len(sensitive_word_string) > 0:
                result.append(sensitive_word_string)
                sensitive_file_list.append(file)
                sensitive_file_path_list.append(file_path)

        elif file_type in compressed_type_list:
            sensitive_word_string = search_compressed_file(file_path, sensitive_word)
            if len(sensitive_word_string) > 0:
                result.append(sensitive_word_string)
                sensitive_file_list.append(file)
                sensitive_file_path_list.append(file_path)

        elif file_type in text_type_list:
            sensitive_word_string = search_text_file(file_path, sensitive_word)
            if len(sensitive_word_string) > 0:
                result.append(sensitive_word_string)
                sensitive_file_list.append(file)
                sensitive_file_path_list.append(file_path)
        else:
            unknown_type_list.append(file_type)

    # =====================step4. 回写结果=====================#
    # 追加写入result
    with open(csv_path, 'a+') as f:
        csv_write = csv.writer(f)
        for i, _ in enumerate(result):
            data_row = [sensitive_file_list[i], result[i], sensitive_file_path_list[i]]
            csv_write.writerow(data_row)


def search_img_file(file_path, sensitive_word):
   pass


def search_text_file(file_path, sensitive_word):
    pass


def search_compressed_file(file_path, sensitive_word):
    pass


if __name__ == '__main__':
    base_path = os.getcwd()
    # 存放主办方自己设置的敏感词
    sensitive_word = ['机密', '绝密']
    search_sensitive_file(base_path, sensitive_word)
