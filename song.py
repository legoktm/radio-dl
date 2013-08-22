#!/usr/bin/python
# -*- coding: utf-8 -*-

import main
import os
import urlparse


class Song:
    def __init__(self, artist, name):
        self.artist = artist
        self.name = name

    def __eq__(self, other):
        return self.name == other.name and self.artist == other.artist

    def __str__(self):
        return self.name + u'-' + self.artist

    def __repr__(self):
        return u'Song({0})'.format(str(self))

    def fetch(self):
        self.yt = main.get_video(self.artist, self.name)
        print self.yt
        if not os.path.exists(self.filename):
            main.download(self.yt)

    @property
    def filename(self):
        q = urlparse.parse_qs(urlparse.urlparse(self.yt)[4])
        return q['v'][0] + '.mp3'

    def play(self):
        main.notify(u'Now playing: {0}'.format(unicode(self)))
        main.playback(self.filename)
