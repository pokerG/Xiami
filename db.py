# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
from HTMLParser import HTMLParser


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

mysql_host = 'localhost'
mysql_port = 3306
mysql_user = 'root'
mysql_password = ''
mysql_db = 'kdwtemp2'
mysql_charset = 'utf8mb4'

mg_host = 'localhost'
mg_port = 27017
mg_user = ''
mg_password = ''

hp = MyHTMLParser()

mgClient = pymongo.MongoClient(mg_host, mg_port)
mgOrigin = mgClient.Xiami.OriginData
# print(mgOrigin.find_one())

mysqlConnection = pymysql.connect(host=mysql_host,
                                  port=mysql_port,
                                  user=mysql_user,
                                  password=mysql_password,
                                  db=mysql_db,
                                  charset=mysql_charset,
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
                hp.releasetime = hp.releasetime.replace('年', '-')
                hp.releasetime = hp.releasetime.replace('月', '-')
                hp.releasetime = hp.releasetime.replace('日', '')
                print '%s %s %s' % (res.get("SongName").encode("utf-8"), res.get("songsterName").encode("utf-8"), hp.releasetime)
                args.append((res.get("SongID").encode("utf-8"), res.get("SongName").encode("utf-8"),
                                     res.get("songsterName").encode("utf-8"), hp.releasetime))

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

