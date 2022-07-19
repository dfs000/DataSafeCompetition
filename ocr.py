# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 15:18
# @Author  : dfs
# @FileName: ocr.py
# @Team    : qingan
# @Describe:
import requests
import base64

def get_baidu_token() -> str:
    """获得百度的token"""
    import requests
    ak = "*" # 第2步中的API Key
    sk = "*" # 第2步中的Secret Key
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
        ak, sk)
    response = requests.get(host)
    if response:
        return response.json()['access_token']

def get_ocr_result():
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open('imgs/img.png', 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = get_baidu_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return (response.json()['word_result'])

def analysis_ocr_result():
    pass