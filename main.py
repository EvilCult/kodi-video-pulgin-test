# -*- coding: utf-8 -*-

import sys
import urllib2
import urlparse
import json
import xbmcgui
import xbmcplugin

_url = sys.argv[0]
_handle = int(sys.argv[1])

def getList():
    jsonStr = urllib2.urlopen('http://***/onepiece.json').read()
    data = json.loads(jsonStr)

    tvDict = {}
    for x in data:
        tvDict[x['number']] = x

    return tvDict

def getChapter():
    tvDict = getList()
    chapList = []
    for x in range(1, len(tvDict) + 1):
        if tvDict[str(x)]['chapter'] not in chapList:
            chapList.append(tvDict[str(x)]['chapter'])

    return chapList

def getVideo(chapter):
    tvDict = getList()
    tvList = []
    for x in range(1, len(tvDict) + 1):
        if tvDict[str(x)]['chapter'].encode('utf-8') == chapter:
            tvList.append(tvDict[str(x)])

    return tvList

def parseRealUrl(url):
    if url.find('iqiyi') > 0:
        api = 'https://app.tf.js.cn/jxds/api.php?url=%s&danmu=0' % (url)
        try:
            jsonStr = urllib2.urlopen(api).read()
            data = json.loads(jsonStr)
            link = data['url']
        except :
            link = ''
    else:
        link = url

    return link

def listChapter():
    xbmcplugin.setPluginCategory(_handle, '海贼王')
    xbmcplugin.setContent(_handle, 'videos')

    chapters = getChapter()
    i = 0
    for chapter in chapters:
        item = xbmcgui.ListItem(label=chapter.encode('utf-8'))

        item.setInfo('video', {'title': chapter.encode('utf-8'), 'mediatype': 'video'})
        url = '{0}?action=listing&chapter={1}'.format(_url, i)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, item, is_folder)
        i += 1

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def listVideo(chapter):
    chapters = getChapter()
    chapTitle = chapters[int(chapter)].encode('utf-8')

    xbmcplugin.setPluginCategory(_handle, chapTitle)
    xbmcplugin.setContent(_handle, 'videos')
    
    videos = getVideo(chapTitle)
    for video in videos:
        title = str(video['number']) + '.' + video['title'].encode('utf-8')
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title, 'mediatype': 'video'})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video={1}'.format(_url, video['link'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def playVideo(path):
    m3u8 = parseRealUrl(path)
    play_item = xbmcgui.ListItem(path=m3u8)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def router(paramstring):
    params = dict(urlparse.parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            listVideo(params['chapter'])
        elif params['action'] == 'play':
            playVideo(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        listChapter()

if __name__ == '__main__':
    router(sys.argv[2][1:])
