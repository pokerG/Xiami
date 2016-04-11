# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
from HTMLParser import HTMLParser
import datetime

import gl

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.found = False
        self.releasetime = ""

    def handle_data(self, data):
        if self.found:
            self.found = False
            self.releasetime = data
        if data.find("发行时间") >= 0:
            self.found = True



hp = MyHTMLParser()

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgOrigin = mgClient.Xiami.OriginData
# print(mgOrigin.find_one())

mysqlConnection = pymysql.connect(host=gl.mysql_host,
                                  port=gl.mysql_port,
                                  user=gl.mysql_user,
                                  password=gl.mysql_password,
                                  db=gl.mysql_db,
                                  charset=gl.mysql_charset,
                                  cursorclass=pymysql.cursors.DictCursor)

try:
    with mysqlConnection.cursor() as cursor:
        sql = "SELECT * FROM kdw_tbl_song"
        cursor.execute(sql)
        num = 0
        n = 0
        args = []
        for res in cursor:
            num += 1
            doc = mgOrigin.find_one({"musics.value": res.get("SongName")})
            if doc:
                album_info = doc.get("album_info").encode("utf-8")
                album_info = album_info.replace('\r', '')
                album_info = album_info.replace('\n', '')
                album_info = album_info.replace('\t', '')
                hp.feed(album_info)
                releasetime = datetime.datetime.strptime(hp.releasetime, "%Y年%m月%d日")
                # hp.releasetime = hp.releasetime.replace('年', '-')
                # hp.releasetime = hp.releasetime.replace('月', '-')
                # hp.releasetime = hp.releasetime.replace('日', '')
                print '%s %s %s' % (res.get("SongName").encode("utf-8"), res.get("songsterName").encode("utf-8"), releasetime.date())
                args.append((res.get("SongID").encode("utf-8"), res.get("SongName").encode("utf-8"),
                                     res.get("songsterName").encode("utf-8"), releasetime.date()))

                n += 1
        print(num)
        print(n)
        insertsql = """
            INSERT INTO `song_info` (`SongID`, `SongName`, `songsterName`, `releaseTime`) VALUES (%s, %s, %s, %s)
            """
        cursor.executemany(insertsql, args)
        # print(result.get("id"))
    mysqlConnection.commit()
finally:
    hp.close()
    mgClient.close()
    mysqlConnection.close()

