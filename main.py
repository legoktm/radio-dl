#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import subprocess
import sh

youtube_dl = sh.Command('youtube-dl')


def get_video(artist, song):
    query = artist.lower() + ' ' + song.lower()
    url = 'https://gdata.youtube.com/feeds/api/videos'
    r = requests.get(url, params={'q': query, 'alt': 'json'})
    #print r.text
    j = r.json()
    vid = j['feed']['entry'][0]['link'][0]['href']
    vid = vid.replace('&feature=youtube_gdata', '')
    return vid


def download(url):
    cmd = 'youtube-dl '
    cmd += url
    cmd += ' --id -x --audio-format mp3 -f worst'
    #youtube_dl(url + '--id')
    c = subprocess.call(
        cmd,
        stderr=subprocess.STDOUT,
        shell=True
    )
    return c


def playback(filename):
    cmd = 'afplay ' + filename
    c = subprocess.call(
        cmd,
        stderr=subprocess.STDOUT,
        shell=True
    )
    return c


def notify(msg):
    cmd = 'terminal-notifier -message "{0}"'.format(msg)
    subprocess.call(
        cmd,
        stderr=subprocess.STDOUT,
        shell=True
    )

