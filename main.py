# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 14:00
# @Author  : dfs
# @FileName: main.py
# @Team    : qingan
# @Describe:
import os
import csv
import time
from ocr import analysis_ocr_result, get_ocr_result
import PyPDF2
import re
from extractor import *


def search_sensitive_file(base_path, sensitive_word):
    # =====================step1. 设置结果写入的文件名称以及读取的文件列表=====================#
    # 获取写入的csv文件名称
    result_path = 'result_' + time.strftime("%Y%m%d-%H:%M:%S") + '.csv'
    with open(result_path, 'w', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        csv_head = ["文件名称", "文件内所含敏感词"]
        csv_write.writerow(csv_head)

    err_path = 'err_' + time.strftime("%Y%m%d-%H:%M:%S") + '.csv'
    with open(err_path, 'w', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        csv_head = ["文件名称", "备注"]
        csv_write.writerow(csv_head)
    # 获取要分析的文件列表
    # 需要递归找到所有文件，应该用os.walk()
    # file_list = os.listdir(base_path)
    file_list_first = []
    file_list = []
    for root, _, files in os.walk('.', topdown=False):
        for name in files:
            file_list_first.append(os.path.join(root, name))

    # result存放的是命中的敏感词
    result = []

    # sensitive_file_list存放的是命中的敏感文件列表，这个跟result是一一对应的
    sensitive_file_list = []

    err_file_list = []

    err_file_reson = []

    # =====================step2. 设置文件类型列表=====================#
    # 图像文件后缀名
    img_type_list = ['.jpg', '.png', '.jpeg']
    # 压缩文件后缀名
    # office类型的文件均可以通过zip解压的方式来分离图片和文本
    compressed_type_list = ['.zip', '.rar', '.7z', '.docx', '.doc', '.ppt', '.pptx', '.xlsx']
    # 能直接读取搜索的文本文件后缀名
    text_type_list = ['.txt', '.xml', 'csv']
    # 需要特殊处理的文件后缀名
    sp_type_list = ['.pdf']

    for file in file_list_first:
        # 获取文件后缀名，判断类型执行相应的查找方法
        file_type = file[file.rfind('.'):]
        try:
            if file_type in compressed_type_list:
                a, b = extract(file)
        except:
            err_file_list.append(file)
            err_file_reson.append("文件解析失败")
            print("解析失败文件：", file)
    for root, _, files in os.walk('.', topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))

    # =====================step3. 遍历每一个文件进行分析，找出含有敏感词的文件=====================#
    for file in file_list:

        # 获取文件后缀名，判断类型执行相应的查找方法
        file_type = file[file.rfind('.'):]

        # 拼接文件的路径
        file_path = base_path + '/' + file
        print("file", file)
        try:
            if file_type in img_type_list:
                pass
                # sensitive_word_string = search_img_file(file, sensitive_word)
                # if sensitive_word_string!= None and len(sensitive_word_string) > 0:
                #     result.append(sensitive_word_string)
                #     sensitive_file_list.append(file)
                #     sensitive_file_path_list.append(file)
            elif file_type in compressed_type_list:
                # 文件解压出来后，分类放置在文件夹中，然后调用对应的处理办法
                # sensitive_word_string = search_pdf_file(file_path, sensitive_word)
                # if sensitive_word_string!= None and len(sensitive_word_string) > 0:
                #     print("=========", sensitive_word_string)
                #     result.append(sensitive_word_string)
                #     sensitive_file_list.append(file)
                continue


            elif file_type in sp_type_list:
                # 文件解压出来后，分类放置在文件夹中，然后调用对应的处理办法

                sensitive_word_string = search_pdf_file(file_path, sensitive_word)
                if sensitive_word_string != None and len(sensitive_word_string) > 0:
                    print("=========", sensitive_word_string)
                    result.append(sensitive_word_string)
                    sensitive_file_list.append(file)


            elif file_type in text_type_list:
                sensitive_word_string = search_text_file(file_path, sensitive_word)
                if sensitive_word_string != None and len(sensitive_word_string) > 0:
                    print("=========", sensitive_word_string)
                    result.append(sensitive_word_string)
                    sensitive_file_list.append(file)

            else:
                err_file_list.append(file)
                err_file_reson.append("未知的文件类型")
        except:
            err_file_list.append(file)
            err_file_reson.append("读取失败")

    # =====================step4. 回写结果=====================#
    # 追加写入result

    with open(result_path, 'a+', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        for i, _ in enumerate(result):
            data_row = [sensitive_file_list[i], result[i]]
            csv_write.writerow(data_row)
    with open(err_path, 'a+', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        for i, _ in enumerate(err_file_list):
            data_row = [err_file_list[i], err_file_reson[i]]
            csv_write.writerow(data_row)


def search_img_file(file_path, sensitive_word):
    text = get_ocr_result(file_path)
    result = []
    for String in sensitive_word:
        ResSearch = re.search(String, text)
        if ResSearch is not None:
            result.append(String)
    return result


def search_compressed_file(file_path, sensitive_word):
    pass


def search_pdf_file(file_path, sensitive_word):
    # import packages
    result = []
    object = PyPDF2.PdfFileReader(file_path)
    # get number of pages
    NumPages = object.getNumPages()
    # extract text and do the search
    for i in range(0, NumPages):
        PageObj = object.getPage(i)
        print("this is page " + str(i))
        # 需要除去空格来匹配
        Text = PageObj.extractText().replace(" ", "")
        # print(Text)
        for String in sensitive_word:
            ResSearch = re.search(String, Text)
            if ResSearch is not None:
                result.append(String)
    return result


def search_text_file(file_path, sensitive_word):
    result = []
    Text = ''
    with open(file_path) as f:
        s = f.readlines()
        for s_ in s:
            Text += s_.strip('/n')
    for String in sensitive_word:
        ResSearch = re.search(String, Text)
        if ResSearch is not None:
            result.append(String)
    return result


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='manual to this script')
    # 
    # parser.add_argument('--base_path', type=str, default=os.getcwd())
    # parser.add_argument('--sentive_word_text_path', type=str, default='sentitive_word.txt')
    # args = parser.parse_args()
    base_path = "./"
    # 存放主办方自己设置的敏感词
    sensitive_word = ['机密', '绝密']
    search_sensitive_file(base_path, sensitive_word)