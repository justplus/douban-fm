#!/usr/bin/env python
# coding=utf-8
import subprocess
import getch
from termcolor import colored
from api import Api


class Client(object):
    def __init__(self):
        self.api = Api()
        ###
        self.api.login('*', '*')
        self.api.get_channels()

        self.lines, self.columns = self._terminal_size()
        self.margin_left = 0

    def print_title(self):
        subprocess.call('clear', shell=True)
        print ''
        title = 'douban FM  ☻  %s' % self.api.user_name
        self.margin_left = (self.columns - self._str_length(title))/2
        print '%s%s' % (' ' * self.margin_left, colored(title, 'yellow'))
        print ''

    def print_channels(self):
        for i in range(min(self.lines, len(self.api.channels)) - 4):
            print '%s%s' % (' ' * (self.margin_left - 10), self.api.channels[i]['name'])

    def print_channel_page(self):
        while True:
            self.print_title()
            self.print_channels()
            ch = getch._Getch()
            k = ch()

    def _terminal_size(self):
        size = subprocess.check_output('stty size', shell=True)
        size = size.split(' ')
        return int(size[0]), int(size[1])

    def _str_length(self, string):
        length = 0
        for i in string:
            length += (2 if 0x4e00 <= ord(i) < 0x9fa6 else 1)
        return length

if __name__ == '__main__':
    client = Client()
    client.print_channel_page()

