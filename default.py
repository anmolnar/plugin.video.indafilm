# -*- coding: utf-8 -*-
import json
import re
import requests
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import sys


def categories():
    addDir3('Mozifilmek', 'http://film.indavideo.hu/browse/mozifilm', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')
    addDir3('Tévéfilmek', 'http://film.indavideo.hu/browse/tevefilm', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')
    addDir3('Kisfilmek', 'http://film.indavideo.hu/browse/kisfilm', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')
    addDir3('Dokumentumfilmek', 'http://film.indavideo.hu/browse/dokumentumfilm', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')
    addDir3('Természetfilmek', 'http://film.indavideo.hu/browse/termeszetfilm', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')
    addDir3('Animációs filmek', 'http://film.indavideo.hu/browse/animaciosfilm', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')
    addDir3('Magyar Filmhét', 'http://film.indavideo.hu/browse/filmhet', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')
    addDir3('Dokuszemle', 'http://film.indavideo.hu/browse/dokuszemle', 1, 'http://i.imgur.com/BbYiMBc.png',
            'http://i.imgur.com/3aOYSlT.jpg', '')


def indaFolder(url):
    r = requests.get(url)
    match = re.compile('TYPE_24.+?item_type.+?href="(.+?)" class="image.+?"crop"><img src="(.+?)" alt="thumb".+?"title_duration_year"><a href=".+?" >(.+?)</a>.+?"description">(.+?)</div>', re.DOTALL).findall(r.content)
    for url, img, name, desc in match:
        addDir4(name, url, 2, 'http:' + img, 'http:' + img, desc)
    return


def indaVideo(url):
    r = requests.get(url)
    match = re.compile('indavideo\.hu/player/video/([0-9a-f]+)').findall(r.content)
    r = requests.get('http://amfphp.indavideo.hu/SYm0json.php/player.playerHandler.getVideoData/' + match[0])

    videodata = json.loads(r.content)
    video_files = videodata['data']['video_files']
    video_files.sort(reverse=True)
    print('Video files found:')
    print(video_files)
    match = re.compile('\.([0-9]+)\.mp4').findall(video_files[0])
    resolution = match[0]
    print('Selected resolution: ' + resolution)
    token = videodata['data']['filesh'][resolution]
    video_file = video_files[0] + '&token=' + token

    videoitem = xbmcgui.ListItem(label=url, thumbnailImage='http://i.imgur.com/BbYiMBc.png')
    videoitem.setInfo(type='Video', infoLabels={'Title': url})
    xbmc.Player().play(video_file, videoitem)
    return


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def addDir3(name, url, mode, iconimage, fanart, description):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addDir4(name, url, mode, iconimage, fanart, description):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


params = get_params()
url = None
name = None
mode = None
iconimage = None
fanart = None
description = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    fanart = urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    description = urllib.unquote_plus(params["description"])
except:
    pass

if mode is None or url is None or len(url) < 1:
    categories()
elif mode == 1:
    indaFolder(url)
elif mode == 2:
    indaVideo(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
