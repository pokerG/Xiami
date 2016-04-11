# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
import datetime

import gl

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgUserSongSheet = mgClient.Xiami.UserSongSheet
mgUserSongSheetTimeStatis = mgClient.Xiami.UserSongSheetTimeStatis

mysqlConnection = pymysql.connect(host=gl.mysql_host,
                                  port=gl.mysql_port,
                                  user=gl.mysql_user,
                                  password=gl.mysql_password,
                                  db=gl.mysql_db,
                                  charset=gl.mysql_charset,
                                  cursorclass=pymysql.cursors.DictCursor)

try:
    with mysqlConnection.cursor() as cursor:
        sql = "SELECT * FROM song_info where SongID=%s"
        for user in mgUserSongSheet.find():
            statis = {}
            for song in user.get("songsheet"):
                cursor.execute(sql, song.get("songID"))
                result = cursor.fetchone()
                if result:
                    date = str(result.get("releaseTime").year)
                    if date in statis:
                        statis[date] += 1
                    else:
                        statis[date] = 1
            print "%s %s" % (user.get("userid"), statis)
            userstatis = {}
            userstatis["userid"] = user.get("userid")
            userstatis["timeMap"] = statis
            mgUserSongSheetTimeStatis.insert_one(userstatis)

finally:
    mgClient.close()
    mysqlConnection.close()
