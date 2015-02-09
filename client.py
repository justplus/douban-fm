#!/usr/bin/env python
# coding=utf-8
import subprocess
import getch
from termcolor import colored
from api import Api
import keymap


class Client(object):
    def __init__(self):
        subprocess.call('echo  "\033[?25l"', shell=True)
        self.api = Api()
        ###
        self.api.login('*', '*')
        self.api.get_channels()

        self.lines, self.columns = self._terminal_size()
        self.margin_left = 0

        self.channel_ids = []
        self.channel_names = []
        self.selected_line = 0
        self.selected_channel_line = 0

    def print_title(self):
        subprocess.call('clear', shell=True)
        print ''
        title = 'douban FM  ☻  %s' % self.api.user_name
        self.margin_left = (self.columns - self._str_length(title))/2
        print '%s%s' % (' ' * self.margin_left, colored(title, 'yellow'))
        print ''

    def print_channels(self):
        if not self.channel_names:
            for channel in self.api.channels:
                self.channel_names.append(channel['name'])
                self.channel_ids.append(channel['channel_id'])
        if self.selected_line < self.lines - 4:
            start_line = 0
            end_line = min(self.lines - 4, len(self.api.channels))
        else:
            start_line = self.selected_line + 5 - self.lines
            end_line = self.lines - 4 + start_line
        for i in range(start_line, end_line):
            if i == self.selected_channel_line:
                if self.api.song:
                    print u'%s%s%s%s' % (' ' * (self.margin_left - 10), colored(self.channel_names[i], 'cyan'), ' ' * 8, colored(u'%s ● %s' % (self.api.song['title'], self.api.song['artist']), 'cyan'))
                else:
                    print colored(u'%s%s' % (' ' * (self.margin_left - 10), self.channel_names[i]), 'cyan')
            elif i == self.selected_line and i != self.selected_channel_line:
                print '%s%s' % (' ' * (self.margin_left - 10), colored(self.channel_names[i], 'yellow'))
            else:
                print '%s%s' % (' ' * (self.margin_left - 10), self.channel_names[i])

    def print_channel_page(self):
        while True:
            self.print_title()
            self.print_channels()
            ch = getch._Getch()
            k = ch()
            if k == keymap.keys['UP']:
                if self.selected_line == 0:
                    self.selected_line == 0
                else:
                    self.selected_line -= 1
            elif k == keymap.keys['DOWN']:
                if self.selected_line == len(self.channel_names) - 1:
                    self.selected_line = len(self.channel_names) - 1
                else:
                    self.selected_line += 1
            elif k == keymap.keys['SURE']:
                self.api.song = None
                self.selected_channel_line = self.selected_line
                self.api.channel_id = self.channel_ids[self.selected_line]
                self.api.get_playlist()
                self.api.get_song()
                self.api.get_song()
                command = '/Applications/VLC.app/Contents/MacOS/VLC --quiet --intf dummy ' + self.api.song['url']
                subprocess.call(command, shell=True)
            elif k == keymap.keys['QUIT']:
                break

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

