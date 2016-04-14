# -*- coding:utf-8 -*-
import pymongo

import gl

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgUserSongSheetTimeStatis = mgClient.Xiami.UserSongSheetTimeStatis

for user in mgUserSongSheetTimeStatis.find():
    section = {}
    for tuple in user.get('timeMap').items():
        x = str(int(tuple[0]) / 5 * 5 )
        if x in section:
            section[x] += tuple[1]
        else:
            section[x] = tuple[1]
    statis = sorted(section.items(), key=lambda d: d[1], reverse=True)
    print statis
    with open('agemodel.log', 'a') as f:
        if len(statis):
            f.write(user.get('userid') + ' ' + str(statis[0][0]) + '\n')

