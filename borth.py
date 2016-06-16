# -*- coding:utf-8 -*-
import pymongo

import gl

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgExtract = mgClient.Xiami.ExtractData

for song in mgExtract.find():
    singerinfo = ''
    for tuple in song.get('singer_info').items():
        if tuple[0] == '档案':
            singerinfo = tuple[1].encode('utf-8')
            