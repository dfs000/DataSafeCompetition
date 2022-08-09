# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 16:00
# @Author  : allen
# @FileName: extractor.py
# @Team    : qingan
# @Describe:
import os
import zipfile
import shutil
import py7zr
import rarfile

def extract(file_path):
    # 返回一个文本文件夹路径和图片文件夹路径
    # 获取文件后缀名，判断类型执行相应的查找方法
    file_type = file_path[file_path.rfind('.'):]
    # office类型的文件均可以通过zip解压的方式来分离图片和文本
    office_type = ['.docx', '.doc', '.ppt', '.pptx', '.xlsx', '.zip']
    compressed_file_type = ['.7z', '.rar']
    img_type_list = ['.jpg', '.png', 'jpeg']
    text_info_type_list = ['.txt', '.xml']
    if file_type in office_type:
        root_path =  file_path[:file_path.rfind('.')]
        img_path = root_path + '/img'
        xml_path = root_path + '/xml'
        with zipfile.ZipFile(file_path) as f:
            for file in f.namelist():
                file_type = file[file.rfind('.'):]
                if file_type in img_type_list:
                    f.extract(file, path=img_path)
                elif file_type == '.xml':
                    f.extract(file, path=xml_path)
    elif file_type in compressed_file_type:
        root_path =  file_path[:file_path.rfind('.')]
        if file_type == '.rar':
            img_path = root_path + '/img'
            text_info_path = root_path + '/text_info'
            with rarfile.RarFile(file_path) as f:
                for file in f.namelist():
                    file_type = file[file.rfind('.'):]
                    if file_type in img_type_list:
                        f.extract(file, path=img_path)
                    elif file_type in text_info_type_list:
                        f.extract(file, path=text_info_path)
        elif file_type == '.7z':
            img_path = root_path + '/img'
            text_info_path = root_path + '/text_info'
            with py7zr.SevenZipFile(file_path) as f:
                for file in f.getnames():
                    file_type = file[file.rfind('.'):]
                    if file_type in img_type_list:
                        f.extract(file, path=img_path)
                    elif file_type in text_info_type_list:
                        f.extract(file, path=text_info_path)
    return img_path, xml_path

