# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
import datetime

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

mgClient = pymongo.MongoClient(mg_host, mg_port)
mgUserSongSheet = mgClient.Xiami.UserSongSheet

mysqlConnection = pymysql.connect(host=mysql_host,
                                  port=mysql_port,
                                  user=mysql_user,
                                  password=mysql_password,
                                  db=mysql_db,
                                  charset=mysql_charset,
                                  cursorclass=pymysql.cursors.DictCursor)

try:
    with mysqlConnection.cursor() as cursor:
        sql = 'SELECT distinct customerid FROM kdw_tbl_song_menu_event_statics'
        cursor.execute(sql)
        cids = []
        docs = []
        for cid in cursor:
            cids.append(cid.get("customerid").encode("utf-8"))
        for cid in cids:
            sql = "SELECT * FROM kdw_tbl_song_menu_event_statics where customerid=%s"
            cursor.execute(sql, cid)
            doc = {}
            doc['userid'] = cid
            doc['songsheet'] = []
            songinfo = {}
            for line in cursor:
                songinfo['songID'] = line.get("songId").encode("utf-8")
                songinfo['songTime'] = datetime.datetime.strptime(str(line.get("updateDate")), '%Y-%m-%d')
                doc['songsheet'].append(songinfo)
            docs.append(doc)
            print(doc)
            mgUserSongSheet.insert_one(doc)
        # mgUserSongSheet.insert_many(docs)

finally:
    mgClient.close()
    mysqlConnection.close()