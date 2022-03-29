# -*- coding: utf-8 -*-
# author: cgcel

import os

import requests
from tqdm import tqdm

url_main = 'https://shop.vistopia.com.cn/'
url_articles = 'https://api.vistopia.com.cn/api/v1/content/article_list?api_token=null&content_id={}&api_token=null&count={}'
url_content_info = 'https://api.vistopia.com.cn/api/v1/content/content-show/{}?api_token=&content_channel='


class VISTOPIA():
    def __init__(self) -> None:
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': 'Hm_lvt_5e6a1cf9cb572a0995800d3c9062d28c=1648466267; user_tk=null; Hm_lpvt_5e6a1cf9cb572a0995800d3c9062d28c=1648468417',
            'referer': 'https://shop.vistopia.com.cn/index',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_content_info_from_url(self, url: str):
        """get_content_info_from_url

        Args:
            url (str): visitopia article_list url
        """
        param = url.split('=')[-1]
        resp = self.session.get(url_content_info.format(param)).json()
        self.title = resp['data']['title']
        self.content_id = resp['data']['content_id']
        self.article_count = resp['data']['article_count']

    def get_articles_data(self, url: str):
        """get_articles_data

        Args:
            url (str): visitopia article_list url

        Returns:
            json: articles json data
        """
        self.get_content_info_from_url(url)
        resp = self.session.get(url_articles.format(
            self.content_id, self.article_count)).json()
        # for i in resp['data']['article_list']:
        #     print(i['title'])
        return resp

    def download_articles(self, url: str):
        """download_articles

        Args:
            url (str): visitopia article_list url
        """
        articles_data_json = self.get_articles_data(url=url)
        if not os.path.exists(self.title):
            os.makedirs(self.title)

        # 开始下载

        # 消除特殊字符
        intab = "?*/\|.:><"
        outtab = "         "
        trantab = str.maketrans(intab, outtab)

        articles = articles_data_json['data']['article_list']
        for article in articles:
            mp3_title = article['title'].translate(trantab)

            mp3_url = article['media_key_full_url']
            resp = self.session.get(mp3_url)

            total_size_in_bytes = int(resp.headers.get('content-length', 0))
            block_size = 1024
            with open('{}/{}.mp3'.format(self.title, mp3_title), 'wb') as f:
                with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True) as pbar:
                    for data in resp.iter_content(block_size):
                        f.write(data)
                        pbar.update(len(data))


if __name__ == '__main__':
    VISTOPIA().download_articles('https://shop.vistopia.com.cn/detail?id=TwTtq')
