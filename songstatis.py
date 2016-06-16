# -*- coding:utf-8 -*-
import pymongo
import sys

import gl

reload(sys)
sys.setdefaultencoding('utf-8')

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgUserSongSheet = mgClient.Xiami.UserSongSheet
mgExtractData = mgClient.Xiami.ExtractData

document = mgUserSongSheet.find_one({"userid":"1062"})
songsheet = document.get('songsheet')
songdistri = {}
singerdistri = {}
for song in songsheet:
    songname = song.get('songName')
    songdoc = mgExtractData.find_one({'$or':[{'music_title':songname}, {'music_alias': songname}]})
    if songdoc != None:
        singername = songdoc.get('singer_title')
        if singername in singerdistri:
            singerdistri[singername] += 1
        else:
            singerdistri[singername] = 1
        print singername
    if songname in songdistri:
        songdistri[songname] += 1
    else:
        songdistri[songname] = 1
sortedsingerdistri = sorted(singerdistri.iteritems(), key=lambda x:x[1], reverse=True)
sortedsongdistri = sorted(songdistri.iteritems(), key=lambda x:x[1], reverse=True)
for i in range(0, 10):
    print sortedsongdistri[i][0],sortedsongdistri[i][1]
for i in range(0, 10):
    print sortedsingerdistri[i][0],sortedsongdistri[i][1]