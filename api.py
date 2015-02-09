#!/usr/bin/env python
# coding=utf-8
import requests
import simplejson
import os
import urllib


class Api(object):
    def __init__(self):
        self.config_path = os.path.expanduser('~/.douban_fm_cfg')
        self.channels = []
        self.channel_id = None
        self._user_data = {}
        self.playlist = []
        self.song = None
        self.user_name = ''

    def login(self, account, password):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self._user_data = simplejson.loads(f.readline())
        else:
            post_data = {
                'app_name': 'radio_desktop_win',
                'version': '100',
                'email': account,
                'password': password
            }
            result_json = requests.post('http://www.douban.com/j/app/login', post_data)
            result = simplejson.loads(result_json.text)
            if result['r'] == 1:
                print result['err']
            else:
                self._user_data = {
                    'app_name': 'radio_desktop_win',
                    'version': '100',
                    'user_id': result['user_id'],
                    'expire': result['expire'],
                    'token': result['token'],
                    'user_name': result['user_name']
                }
                with open(self.config_path, 'w') as f:
                    simplejson.dump(self._user_data, f)
                print self._user_data
        self.user_name = self._user_data['user_name']

    def get_channels(self):
        result_json = requests.get('http://www.douban.com/j/app/radio/channels')
        result = simplejson.loads(result_json.text)
        self.channels += result['channels']

    def get_playlist(self):
        result = self._operation({'type': 'n', 'channel': self.channel_id})
        self.playlist = result['song']

    def get_song(self):
        if not self.playlist:
            self.get_playlist()
        self.song = self.playlist.pop(0)

    def next(self):
        result = self._operation({'type': 's', 'sid': self.song['sid']})
        self.playlist = result['song']

    def bye(self):
        result = self._operation({'type': 'b', 'sid': self.song['sid']})
        self.playlist = result['song']

    def like(self):
        result = self._operation({'type': 'r', 'sid': self.song['sid']})
        self.playlist = result['song']

    def unrate(self):
        result = self._operation({'type': 'u', 'sid': self.song['sid']})
        self.playlist = result['song']

    def end(self):
        self._operation({'type': 'e', 'sid': self.song['sid']})

    def _operation(self, data):
        post_data = self._user_data.copy()
        for d in data.keys():
            post_data[d] = data[d]
        result_json = requests.get('http://www.douban.com/j/app/radio/people?' + urllib.urlencode(post_data))
        return simplejson.loads(result_json.text)


if __name__ == '__main__':
    api = Api()
    api.login('*', '*')

    api.get_channels()
    print api.channels

    api.channel_id = 1
    api.get_playlist()
    print api.playlist

    api.get_song()

    import subprocess
    command = '/Applications/VLC.app/Contents/MacOS/VLC --quiet --intf dummy ' + api.song['url']
    subprocess.call(command, shell=True)