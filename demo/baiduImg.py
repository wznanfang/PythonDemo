import json
import os
import random
import string
import requests
import time


def get_images_from_baidu(keyword, page_num, save_dir):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48'}
    # 请求的 url
    url = 'https://image.baidu.com/search/acjson?'
    n = 0
    for pn in range(0, 10 * page_num, 10):
        # 添加随机休眠时间
        # time.sleep(random.randint(0, 2))
        # 请求参数
        param = {'tn': 'resultjson_com',
                 'ipn': 'rj',
                 'ct': 201326592,
                 'is': '',
                 'fp': 'result',
                 'queryWord': keyword,
                 'cl': 2,
                 'lm': -1,
                 'ie': 'utf-8',
                 'oe': 'utf-8',
                 'adpicid': '',
                 'st': -1,
                 'z': '',
                 'ic': '',
                 'hd': '',
                 'latest': '',
                 'copyright': '',
                 'word': keyword,
                 's': '',
                 'se': '',
                 'tab': '',
                 'width': '1920',
                 'height': '1080',
                 'face': 0,
                 'istype': 2,
                 'qc': '',
                 'nc': '1',
                 'fr': '',
                 'expermode': '',
                 'force': '',
                 'cg': '',  # 这个参数没公开，但是不可少
                 'pn': pn,  # 显示：30-60-90
                 'rn': '10',  # 每页显示 10 条
                 'gsm': '3c',
                 '1682234819814': '',
                 }
        # 发送请求
        request = requests.get(url=url, headers=header, params=param)
        if request.status_code == 200:
            request.encoding = 'utf-8'
            # 正则方式提取图片链接
            html = request.text
            image_url_list = json.loads(html)['data']
            for image_url in image_url_list:
                if image_url:
                    objUrl = image_url['replaceUrl'][0]['ObjURL']
                    print(objUrl)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    image_data = requests.get(url=objUrl, headers=header).content
                    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.jpg'
                    with open(os.path.join(save_dir, file_name), 'wb') as fp:
                        fp.write(image_data)
                    n = n + 1
        else:
            print('-----请求失败-----')


if __name__ == '__main__':
    keyword = '古风'
    save_dir = 'E:/img'
    page_num = 1
    get_images_from_baidu(keyword, page_num, save_dir)
    print('Get images finished.')
