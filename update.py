# coding: utf-8

import socket
from pyquery import PyQuery as pq
import requests
import hashlib
import config

'''
a list of news should be in format of:
{
    category_id: [(news_url, news_title, news_update_date, checksum), ...],
    ...
}
'''


def fetch_news():
    def fetch(url):
        p = pq(requests.get(url).content)
        news_list_html = p('div.xingzheng-txt>ul>li')
        news_list = []
        for news in news_list_html:
            title = pq(news)('a').text()
            url = pq(news)('a').attr('href')
            date = pq(news)('span').text()
            news_list.append((url, title, date, checksum(url, title)))
        return news_list

    def checksum(url, title):
        return hashlib.md5(url + title.encode('utf-8')).hexdigest()

    news = {}
    host = config.HOST
    page_list = config.NEWS_INDEX_PAGE
    for page_id, page_url in page_list.items():
        news[page_id] = fetch(host + page_url)
    return news


def throw_outdated(news_list):
    with open(config.HISTORY_REC_FILE, 'r+') as f:
        history = f.readlines()
        news_list = [news for news in news_list if news[3] not in history]
        history = [news[3] for news in news_list]
        f.writelines(history)
    return news_list


def notify():
    pass


print throw_outdated(fetch_news())
