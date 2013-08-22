#!/usr/bin/python
# -*- coding: utf-8 -*-

import bs4
import requests
from song import Song


class Station:
    def __init__(self):
        self.name = 'BaseStation'

    def fetch(self):
        """
        Subclass this
        @return: list
        """
        return []


class Live105:
    name = 'Live 105.3'

    @staticmethod
    def helper(tag):
        #print tag.has_attr('id')
        if tag.get('class'):
            return tag.get('class')[0] == 'track_info'
        return False

    def fetch(self):
        songs = []
        url = 'http://live105.cbslocal.com/playlist/2013/08/21/'
        r = requests.get(url)
        #print r.text.encode('utf-8')
        soup = bs4.BeautifulSoup(r.text)
        thing = soup.find_all(Live105.helper, recursive=True)
        for x in thing:
            track = artist = False
            for attrib in x.find_all('div'):
                if attrib.get('class'):
                    if attrib.get('class')[0] == 'track_title':
                        track = attrib.get('rel')
                    elif attrib.get('class')[0] == 'track_artist':
                        artist = attrib.get('rel')
            if track and artist:
                songs.append(Song(artist, track))
        songs.reverse()
        #print songs
        return songs

if __name__ == '__main__':
    c = Live105()
    c.fetch()