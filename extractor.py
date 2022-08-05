# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 16:00
# @Author  : allen
# @FileName: extractor.py
# @Team    : qingan
# @Describe:
import os
import zipfile
import py7zr
import rarfile

def extract(file_path):
    # 返回一个文本文件夹路径和图片文件夹路径

    # 获取文件后缀名，判断类型执行相应的查找方法
    file_type = file_path[file_path.rfind('.'):]
    # office类型的文件均可以通过zip解压的方式来分离图片和文本
    office_type = ['.docx', '.doc', '.ppt', '.pptx', '.xlsx']
    compressed_file_type = ['.zip', '.7z', '.rar']
    if file_type in office_type:
        txt_path,img_path = extract_office_file(file_path)
    elif file_path in compressed_file_type:
        txt_path,img_path = extract_compressed_file(file_path)

def extract_office_file(file_path):
    # 解压文本文件和图片文件到指定文件夹 并返回路径
    pass

def extract_compressed_file(file_path):
    # 解压文本文件和图片文件到指定文件夹 并返回路径
    pass
