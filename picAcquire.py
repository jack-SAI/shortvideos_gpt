# 导入 re、requests、traceback、os 和 random 模块
import re # 正则表达式，解析网页
import requests # 请求网页
import traceback
import os
import random # 随机选择
import time
import base64

from config import *



def dowmloadPic(html, keyword, root, startNum, n,max_retry=10):
    headers = {'user-agent': 'Mozilla/5.0'} # 浏览器伪装，因为有的网站会反爬虫，通过该headers可以伪装成浏览器访问，否则user-agent中的代理信息为python
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S) # 找到符合正则规则的目标网站
    num = len(pic_url)
    i = startNum

    subroot = os.path.join(root,keyword)
    os.makedirs(subroot, exist_ok=True)
    txtpath =os.path.join(root,'download_detail.txt') # 修改 txtpath 的赋值

    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')

    pic_urls = [] # 添加一个空列表 pic_urls

    limit = min(60, n - startNum) # 添加一个变量 limit，表示每页最多爬取的图片数量

    def isValidImage(url): # 添加一个函数 isValidImage()，用来判断图片的 url 或者 url 指向的图片是否有效
        response = requests.get(url, headers=headers, timeout=10) # 使用 requests.get() 函数获取图片的响应，并赋给 response 变量
        if response.status_code == 200: # 判断响应的状态码是否为 200，表示成功
            content = response.content # 获取响应的内容，并赋给 content 变量
            if content[:4] == b'\xff\xd8\xff\xe0': # 判断内容的前四个字节是否为 JPG 魔术数字
                return True # 如果是，则返回 True
            elif content[:8] == b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a': # 判断内容的前八个字节是否为 PNG 魔术数字
                return True # 如果是，则返回 True
        return False # 如果响应的状态码不为 200，或者内容的前几个字节不符合 JPG 或 PNG 魔术数字，则返回 False

    for each in pic_url:
        if i < startNum + limit: # 判断 i 是否小于 startNum + limit
            a = '第' + str(i + 1) + '张图片，图片地址:' + str(each) + '\n'
            b = '正在下载' + a
            print(b)
            path = subroot +'\\' + time.strftime("%Y%m%d_%H%M%S")
            retry = 0 # 添加一个变量 retry，用来记录重试次数，并赋值为 0
            # max_retry = 10 # 添加一个变量 max_retry，用来表示最大重试次数，并赋值为 3
            while True: # 添加一个 while 循环，用来重试下载图片
                try: # 添加一个 try 语句，用来捕获可能发生的异常
                    if not os.path.exists(subroot):
                        os.mkdir(subroot)
                    if not os.path.exists(path):
                        if isValidImage(each): # 添加一个 if 语句，用来调用 isValidImage() 函数，判断图片的 url 是否有效
                            pic = requests.get(each, headers=headers, timeout=10) # 如果有效，则继续下载图片
                            with open(path + '.jpg', 'wb') as f:
                                f.write(pic.content)
                                f.close()
                            with open(txtpath, 'a') as f:
                                f.write(a)
                                f.close()
                            pic_urls.append(path + '.jpg') # 将图片的路径追加到 pic_urls 中
                        else: # 如果无效，则抛出一个异常
                            raise Exception('图片无法访问')
                    break # 如果下载成功，跳出循环
                except: # 添加一个 except 语句，用来处理异常
                    traceback.print_exc()
                    print('【错误】当前图片无法下载')
                    retry += 1 # 将重试次数加一
                    if retry > max_retry: # 判断重试次数是否超过最大值
                        break # 如果超过，跳出循环，并抛出一个错误
                        raise Exception('达到最大重试次数')
                    else: # 如果没有超过，继续循环，并从 pic_url 列表中随机选择一个新的 url
                        print('【重试】第 {} 次重试'.format(retry))
                        each = random.choice(pic_url) # 使用 random.choice() 函数，从 pic_url 列表中随机选择一个元素，并赋给 each 变量
            i += 1
        else: # 如果 i 大于等于 startNum + limit，跳出循环
            break

    return i, pic_urls # 返回 i 和 pic_urls 的值

def download_pics(keyword, n, root):
    headers = {'user-agent': 'Mozilla/5.0'}
    n=int(n)
    pages = (n - 1) // 60 + 1  # 根据 n 的值，计算出需要爬取的页数
    lastNum = 0
    pageId = 0
    pic_urls = []  # 添加一个空列表 pic_urls
    count = 0  # 添加一个变量 count，用来记录已经爬取的图片数量，并赋值为 0
    for i in range(pages):  # 修改 for 循环，循环 pages 次
        if count < n:  # 判断 count 是否小于 n
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + "&pn=" + str(
                pageId) + "&gsm=?&ct=&ic=0&lm=-1&width=0&height=0"
            pageId += 1  # 好像没啥影响
            html = requests.get(url, headers=headers)
            # print(html.text) #打印网页源码，相当于在网页中右键查看源码内容
            lastNum, urls = dowmloadPic(html.text, keyword, root, lastNum,
                                             n)  # 修改 dowmloadPic() 函数的调用，传入 keyword、root 和 n 参数，并接收返回的 urls 列表
            pic_urls.extend(urls)  # 将 urls 列表扩展到 pic_urls 中
            count = lastNum  # 将 lastNum 的值赋给 count
        else:  # 如果 count 大于等于 n，跳出循环
            break

    return pic_urls  # 返回 pic_urls 列表

# 定义一个函数来根据关键词生成图片，并保存在本地
def generate_image(keyword, num,project_folder):  # 修改函数参数，增加 num 参数
    num = num.replace('*', '')
    num = int(num)
    subroot = os.path.join(project_folder, keyword)
    image_path = os.path.join(subroot,
                              f"{keyword}")  # 修改图片文件的路径，增加 index 参数
    try:
        if not os.path.exists(subroot):
            os.mkdir(subroot)
        if not os.path.exists(image_path):
                # 调用 openai 的 Image.create 方法，传入关键词、图片数量、图片大小和响应格式参数，得到响应对象
            response = openai.Image.create(
                prompt=keyword,
                n=num,  # 修改 n 参数为 num 变量
                size="256x256",
                response_format="b64_json",
            )

            data = response["data"]
            image_paths = []  # 定义一个空列表 image_paths ，用来存储图片文件的路径
            # 如果列表不为空，继续执行
            if data:
                # 遍历列表中的每个元素，得到一个包含图片数据的字典
                for index, image_dict in enumerate(data):
                    b64_str = image_dict["b64_json"]

                    image_data = base64.b64decode(b64_str)  # 使用 base64 模块的 b64decode() 函数，将 b64_str 解码成二进制数据



                    with open(image_path+f'{index}'+'.png', mode="wb") as file:  # 以二进制写入模式打开文件
                        file.write(image_data)  # 将二进制数据写入文件
                    # 将图片文件的路径字符串追加到 image_paths 列表中
                    image_paths.append(str(image_path+f'{index}'+'.png'))
                # 返回 image_paths 列表
                return image_paths
            # 如果列表为空，返回 None
            else:
                return None
            # 如果发生异常，返回 None
    except Exception as e:
        return None


def get_pics(keywords, n, root):
    pics = []  # 定义一个空列表 pics
    for i in range(len(keywords)):  # 修改遍历方式，使用索引 i 来同时访问 keywords 和 n 两个列表
        keyword = keywords[i]  # 获取 keywords 列表中的第 i 个元素，赋给 keyword 变量
        num = n[i]  # 获取 n 列表中的第 i 个元素，赋给 num 变量
        if num in ['*1', '*2', '*3', '*4', '*5']:  # 修改判断条件，判断 num 是否属于 [1,2,3,4,5] 列表
            root1=os.path.join(root,"imggen")
            print("generate image" + keyword)
            pic_urls = generate_image(keyword, num,root1)  # 调用 generate_image() 方法，传入 keyword 和 num 参数，并接收返回的 pic_urls 列表
        else:
            root1=os.path.join(root,"imgcrawl")
            pic_urls = download_pics(keyword, num,
                                     root1)  # 调用 download_pics() 方法，传入 keyword、num 和 root 参数，并接收返回的 pic_urls 列表
        pic = random.choice(pic_urls)  # 使用 random.choice() 函数，从 pic_urls 列表中随机选择一个元素，并赋给 pic 变量
        pics.append(pic)  # 将 pic 变量追加到 pics 列表中

    return pics  # 返回 pics

if __name__=="__main__":
    address=get_pics(['hollow night,fighting','猫咪'],['*2','2'],'E:\DeskTop\ds2')
    print(address)
    # imggenaddress=generate_image("lion,with wings,flying,realistic", '*2','E:\DeskTop\ds2\imggen')
    # print(imggenaddress)

