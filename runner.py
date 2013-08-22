#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import Queue
import stations
import sys
import threading
import time


# Setup
if not os.path.exists('tmp'):
    os.mkdir('tmp')
os.chdir('tmp')

class BaseThread(threading.Thread):
    def run(self):
        try:
            self._run()
        except KeyboardInterrupt:
            sys.exit()

    def _run(self):
        pass


class FetchThread(BaseThread):
    def __init__(self, queue, station, downloaded):
        self.queue = queue
        self.station = station
        self.downloaded = downloaded
        self.last = None
        threading.Thread.__init__(self)

    def _run(self):
        while True:
            if len(self.downloaded) < 5:
                self.update()
            time.sleep(60)

    def update(self):
        new_songs = self.station.fetch()
        if self.last:
            go = False
            for song in new_songs:
                if not go and (song == self.last):
                    go = True
                    continue
                elif not go:
                    continue
                self.queue.put(song)
        else:
            #print new_songs
            new_songs.reverse()
            last = new_songs[0:5]
            last.reverse()
            new_songs.reverse()
            #print last
            for song in last:
                self.queue.put(song)
                self.last = song  # the last one will stay here


class DownloadThread(BaseThread):
    def __init__(self, queue, push):
        self.queue = queue
        self.push = push
        threading.Thread.__init__(self)

    def _run(self):
        while True:
            song = self.queue.get()
            try:
                song.fetch()
                self.push.put(song)
            except:
                pass
            self.queue.task_done()


class PlayThread(BaseThread):
    def __init__(self, queue):
        self.queue = queue
        threading.Thread.__init__(self)

    def _run(self):
        while True:
            song = self.queue.get()
            song.play()
            self.queue.task_done()

to_fetch = Queue.Queue()
downloaded = Queue.Queue()
station = stations.Live105()
f = FetchThread(to_fetch, station, downloaded)
f.setDaemon(True)
f.start()
d = DownloadThread(to_fetch, downloaded)
d.setDaemon(True)
d.start()
p = PlayThread(downloaded)
p.setDaemon(True)
p.start()
time.sleep(10)
to_fetch.join()
downloaded.join()
