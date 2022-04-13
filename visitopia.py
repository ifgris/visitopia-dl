# -*- coding: utf-8 -*-
# author: cgcel

from asyncio.windows_events import NULL
import csv
import json
import os

import requests
from tqdm import tqdm

url_main = 'https://shop.vistopia.com.cn/'
url_article_list = 'https://api.vistopia.com.cn/api/v1/content/article_list?api_token=null&content_id={}&api_token=null&count={}'
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

        # 消除特殊字符
        intab = "?*/\|.:><"
        outtab = "         "
        self._trantab = str.maketrans(intab, outtab)

    def _get_content_info_from_url(self, url: str):
        """get content info from url

        Args:
            url (str): visitopia article_list url
        """
        param = url.split('=')[-1]
        resp = self.session.get(url_content_info.format(param)).json()
        self.title = resp['data']['title']
        self.content_id = resp['data']['content_id']
        self.article_count = resp['data']['article_count']

    def _get_article_list(self, url: str):
        """get articles data

        Args:
            url (str): visitopia article_list url

        Returns:
            json: articles json data
        """
        self._get_content_info_from_url(url)
        resp = self.session.get(url_article_list.format(
            self.content_id, self.article_count)).json()
        # for i in resp['data']['article_list']:
        #     print(i['title'])
        return resp

    def _generate_basics(self, json_data: json):
        """generate directory and catalog including all titles of contents

        Args:
            url (str): visitopia article_list url
        """
        # 新建存储文件夹
        if not os.path.exists(self.title):
            os.makedirs(self.title)

        # 生成下载目录
        titles = [[x['title'].translate(self._trantab)]
                  for x in json_data['data']['article_list']]
        with open('{}/catalog.csv'.format(self.title), 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(titles)

    def _check_new(self):
        """check for new articles

        Returns:
            bool: _description_
        """
        with open('{}/catalog.csv'.format(self.title), 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            rows = []
            for row in reader:
                try:
                    rows.append(row[0])
                except:
                    pass
            rows = set(rows)
        file_list = set([x.split('.mp3')[0] for x in os.listdir(self.title)])
        self._new_article = list(rows - file_list)
        if len(self._new_article) > 0:
            return True
        else:
            return False

    def download_all(self, url: str):
        """download all contents in article

        Args:
            url (str): visitopia article_list url
        """
        articles_data_json = self._get_article_list(url=url)

        self._generate_basics(json_data=articles_data_json)

        if self._check_new():
            print('New article found!')

            # 开始下载
            articles = articles_data_json['data']['article_list']
            for article in articles:
                media_title = article['title'].translate(self._trantab)
                if media_title in self._new_article:
                    # 判定media是否为音频/视频
                    media_url = ''
                    if article['media_key_full_url'] != None and article['sample_media_full_url'] == None:
                        media_url = article['media_key_full_url']
                        media_type = 'mp3'
                    elif article['media_key_full_url'] == None and article['sample_media_full_url'] != None:
                        media_url = article['sample_media_full_url']
                        media_type = 'mp4'
                    resp = self.session.get(media_url)

                    total_size_in_bytes = int(
                        resp.headers.get('content-length', 0))
                    block_size = 1024
                    with open('{}/{}.{}'.format(self.title, media_title, media_type), 'wb') as f:
                        with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True) as pbar:
                            for data in resp.iter_content(block_size):
                                f.write(data)
                                pbar.update(len(data))
        else:
            print('No update articles found! Exit...')
            pass

    def download_single(self, article_id):
        """_summary_

        Args:
            article_id (_type_): _description_
        """
        pass


if __name__ == '__main__':
    VISTOPIA().download_all('https://shop.vistopia.com.cn/detail?id=234')
