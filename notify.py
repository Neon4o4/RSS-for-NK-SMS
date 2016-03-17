# coding: utf-8

import socket
import os

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

    def notify(self, mail_addr_list):
        pass

    def run(self):
        pass
