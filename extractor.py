# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 15:18
# @Author  : dfs
# @FileName: ocr.py
# @Team    : qingan
# @Describe:
import requests
import base64
import json

def get_baidu_token() -> str:
    """获得百度的token"""
    import requests
    ak = "uw5qSuFMDsphFOoyevufnYKf" # 第2步中的API Key
    sk = "UO9VnEzIfYnNlgQcW6ITnlo6b9lg2tjO" # 第2步中的Secret Key
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
        ak, sk)
    response = requests.get(host)
    if response:
        return response.json()['access_token']

def get_ocr_result(img_path):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = get_baidu_token()
    # print(access_token)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    result = ""
    if response:

        data = json.loads(response.text).get("words_result")
        # data.get()
        # print(data)
        for k in data:
            result = result + " "+ k.get('words')
            # result.append(k.get('words'))
    # print(result)
    return result

def analysis_ocr_result():
    pass

#
if __name__ == '__main__':
    img_path = 'imgs/img.png'
    get_ocr_result(img_path)