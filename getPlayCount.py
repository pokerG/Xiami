# -*- coding:utf-8 -*-
import pymongo
import httplib
import datetime
import logging
import copy
import traceback

import gl

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgExtract = mgClient.Xiami.ExtractData

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='getplaycount.log',
                    filemode='w')

def getPlayCount(uid, utype):
    conn = httplib.HTTPConnection("www.xiami.com")
    url = '/count/getplaycount?id=%s&type=%s' % (uid, utype)
    conn.request('GET', url)
    response = eval(conn.getresponse().read())
    conn.close()
    return response.get("plays")

t1 = datetime.datetime.now()
documents = copy.deepcopy(mgExtract.find())
try:
    for document in documents:
        print document.get('_id')
        songplaycount = 0
        artistplaycount = 0
        songid = document.get('music_href')[document.get('music_href').rfind('/') + 1:]
        artistid = document.get('singer_href')[document.get('singer_href').rfind('/') + 1:]
        for i in range(0, 3):
            try:
                songplaycount = getPlayCount(songid, 'song')
            except Exception, e:
                debuginfo = '%s  id %s song %d times request failed' % (str(e), str(songid), i + 1)
                print debuginfo
                logging.debug(debuginfo)
            else:
                break
        for i in range(0, 3):
            try:
                artistplaycount = getPlayCount(artistid, 'artist')
            except Exception, e:
                debuginfo = '%s  id %s artist %d times request failed' % (str(e), str(artistid), i + 1)
                print debuginfo
                logging.debug(debuginfo)
            else:
                break
        print "update %s : %d %d" % (document.get('_id'), songplaycount, artistplaycount)
        mgExtract.update_one({"_id": document.get('_id')}, {"$set": {"music_count.play": songplaycount, "singer_count.play": artistplaycount}})
except Exception, e:
    print traceback.format_exc()
    print e
finally:
    mgClient.close()


