
import os.path
import time

import requests

import urllib.parse
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urlencode

from config import *

BAIDU_API_KEY = "iYbU5qD7NI7WQfZoxupGGtaG"
BAIDU_SECRET_KEY = "aYGMc1cuwfoLr58vFprRj7p4HX2bGtx7"

def text2audio(project_dir,tex):
    url = "https://tsn.baidu.com/text2audio"
    token = get_access_token()
    texprased = urllib.parse.quote_plus(tex)
    # print(texprased)
    payload = 'tex=' + texprased + '&tok=' + token + '&cuid=111222333&ctp=1&lan=zh&per=1'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)

    result_str = response.content

    # if response.status_code==200:
    if response.status_code == 200:
        # save_file = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.' + 'mp3'
        # save_file =videos_folder+'\\audios\\'+ tex + '.' + 'mp3'
        save_file = os.path.join(project_dir, 'audios', tex + '.mp3')

        # save_file = videos_folder + '\\audios\\' + 'abc.mp3'
        print(save_file)
        with open(save_file, 'wb') as of:
            of.write(result_str)
        print(tex)
        print('success!')
    else:
        print('error:' + response.status_code)
    return save_file


def textlist2audio(project_dir,texlist):
    # 定义一个空列表，用于存储生成的音频文件的地址
    save_files_list = []
    # 遍历文本列表中的每个元素
    for tex in texlist:
        # 调用原来的方法，传入文本元素作为参数，并得到音频文件地址
        save_file = text2audio(project_dir,tex)
        # 将音频文件地址添加到列表中
        save_files_list.append(save_file)
    # 返回列表作为结果
    return save_files_list


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": BAIDU_API_KEY, "client_secret": BAIDU_SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))