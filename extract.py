# -*- coding:utf-8 -*-
import pymongo
import httplib
import sys
import datetime

import gl
import myhtmlparser

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgOrigin = mgClient.Xiami.OriginData
mgExtract = mgClient.Xiami.ExtractData

# HTML解析时碰到转义字符出错
reload(sys)
sys.setdefaultencoding('utf-8')

def getPlayCount(uid, utype):
    conn = httplib.HTTPConnection("www.xiami.com")
    url = '/count/getplaycount?id=%s&type=%s' % (uid, utype)
    conn.request('GET', url)
    response = eval(conn.getresponse().read())
    conn.close()
    return response.get("plays")


countParser = myhtmlparser.countHTMLParser()
tagsParser = myhtmlparser.tagsHTMLParser()
infoParser = myhtmlparser.infoHTMLParser()

t1 = datetime.datetime.now()
for raw in mgOrigin.find():
    print raw.get('_id')
    for key in raw:
        if raw.get(key) == None:
            raw[key] = ''
    dealedData = {}
    dealedData['music_title'] = raw.get('musics').get('value').encode("utf-8")
    dealedData['music_alias'] = raw.get('music_title').encode("utf-8")
    dealedData['music_href'] = raw.get('musics').get('href').encode("utf-8")
    # playcount = getPlayCount(dealedData['music_href'][dealedData['music_href'].rfind('/')+1:], 'song')
    countParser.refresh()
    countParser.feed(raw.get('music_count').encode("utf-8"))
    dealedData['music_count'] = {"play": 0,
                                 "share": countParser.sharecount,
                                 "comment": countParser.commentcount}
    tagsParser.refresh()
    tagsParser.feed(raw.get('music_tags').encode("utf-8"))
    dealedData['music_tags'] = tagsParser.tags
    infoParser.refresh()
    infoParser.feed(raw.get('music_info').encode("utf-8"))
    dealedData['music_info'] = infoParser.info

    dealedData['album_title'] = raw.get('album_links').get('value').encode("utf-8")
    dealedData['album_alias'] = raw.get('album_title').encode("utf-8")
    dealedData['album_href'] = raw.get('album_links').get('href').encode("utf-8")
    countParser.refresh()
    countParser.feed(raw.get('album_count').encode("utf-8"))
    dealedData['album_count'] = {"play": 0,
                                 "collect": countParser.collectcount,
                                 "comment": countParser.commentcount}
    tagsParser.refresh()
    tagsParser.feed(raw.get('album_tags').encode("utf-8"))
    dealedData['album_tags'] = tagsParser.tags
    infoParser.refresh()
    infoParser.feed(raw.get('album_info').encode("utf-8"))
    dealedData['album_info'] = infoParser.info

    singerName = raw.get('singers_link').get('value').encode("utf-8")
    dealedData['singer_title'] = singerName[0:singerName.find('(')] if singerName.find('(') > 0 else singerName
    dealedData['singer_alias'] = singerName[singerName.find('(') + 1:-1] if singerName.find('(') > 0 else ''
    dealedData['singer_href'] = raw.get('singers_link').get('href').encode("utf-8")
    # playcount = getPlayCount(dealedData['singer_href'][dealedData['singer_href'].rfind('/') + 1:], 'artist')
    countParser.refresh()
    countParser.feed(raw.get('singer_count').encode("utf-8"))
    dealedData['singer_count'] = {"play": 0,
                                 "fans": countParser.fanscount,
                                 "comment": countParser.commentcount}
    tagsParser.refresh()
    tagsParser.feed(raw.get('singer_tag').encode("utf-8"))
    dealedData['singer_tags'] = tagsParser.tags
    infoParser.refresh()
    infoParser.feed(raw.get('singer_info').encode("utf-8"))
    dealedData['singer_info'] = infoParser.info
    print '%s %s %s' % (dealedData['music_title'], dealedData['album_title'], dealedData['singer_title'])
    mgExtract.insert_one(dealedData)

t2 = datetime.datetime.now()
print (t1, t2)
countParser.close()
tagsParser.close()
infoParser.close()
mgClient.close()
