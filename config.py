# coding: utf-8

HOST = 'http://sms.nankai.edu.cn'
NEWS_INDEX_PAGE = {
    'kydt': '/html/kydt/all',
    'xwzx': '/html/xwzx/xyxw',
    'bksjx': '/html/bksjx/all',
    'yjsjx': '/html/yjsjx/all',
    'xsgz': '/html/xsgz/all',
    'zsxx': '/html/zsxx/all',
}  # 科研动态，学院新闻，本科生教育，研究生教育，学生工作，公共数学
HISTORY_REC_FILE = 'fetch_history'
NOTIFYING_SOCK = 'notify.sock'
NOTIFY_LIST = 'to_notify.json'
REGISTER_CHK = 'register_checking'

mail_sender = 'no-reply@service.clatter.cn'
