# coding: utf-8

import socket
import os
import errno
import requests
from pyquery import PyQuery as pq
import smtplib
from email.mime.text import MIMEText
import config

NOTIFYING_SOCK = 'notify.sock'


class Notifier:
    def __init__(self, sock_addr):
        self.notify_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock_addr = sock_addr
        try:
            os.unlink(self.sock_addr)
        except OSError:
            if os.path.exists(self.sock_addr):
                raise
        self.notify_sock.bind(self.sock_addr)
        self.notify_sock.listen(1)

    def gen_notification_content(self, url):
        url = config.HOST + url
        page = requests.get(url).content
        page = pq(page)
        title = page('div#neirong-main>div>h2').text()
        date = page('div#neirong-main>div.tools.fc2.tCenter').text()
        page = page('div.content')
        page('div.tools').remove()
        content = page.html()
        return title, ''.join((
            '<html><body>',
            '<h2>{}</h2>'.format(title),
            '<p align="center"><span>{}</span>'.format(date),
            '<pre>    </pre>',
            u'<a href="{}">点此阅读原文</a></p>'.format(url),
            '<hr />',
            content,
            '</body></html>'
        ))

    def send(self, title, msg, to, mode='html'):
        import config
        content = MIMEText(msg.encode('utf-8'), mode)
        for addr in to:
            content['To'] = addr
        content['From'] = config.mail_sender
        content['Subject'] = title
        smtplib.SMTP('localhost').sendmail(
            config.mail_sender, to, content.as_string()
        )

    def notify(self, addr, url):
        title, msg = self.gen_notification_content(url)
        self.send(title, msg, addr)

    def handle_request(self, r):
        pass

    def run(self):
        while True:
            try:
                sock, addr = self.notify_sock.accept()
                msg = []
                data = sock.recv(8192)
                while len(data):
                    msg.append(data)
                    data = sock.recv(8192)
                msg = ''.join(msg)
                self.notify(msg)
            except IOError as e:
                code, msg = e.args
                # accept may be interrupted because it is
                # so called "slow system call"
                # restart it if that happened
                if code == errno.EINTR:
                    continue
                else:
                    raise


def test():
    url = '/html/kydt/xsjl01/2956.html'
    to = '978463439@qq.com'
    n = Notifier(NOTIFYING_SOCK)
    n.notify([to], url)

test()
