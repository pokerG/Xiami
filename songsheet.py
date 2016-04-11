# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
import datetime

import gl

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgUserSongSheet = mgClient.Xiami.UserSongSheet

mysqlConnection = pymysql.connect(host=gl.mysql_host,
                                  port=gl.mysql_port,
                                  user=gl.mysql_user,
                                  password=gl.mysql_password,
                                  db=gl.mysql_db,
                                  charset=gl.mysql_charset,
                                  cursorclass=pymysql.cursors.DictCursor)

try:
    with mysqlConnection.cursor() as cursor:
        sql = 'SELECT distinct customerid FROM kdw_tbl_song_menu_event_statics'
        cursor.execute(sql)
        cids = []
        docs = []
        for cid in cursor:
            cids.append(cid.get("customerid").encode("utf-8"))
        t1 = datetime.datetime.now()
        for cid in cids:
            sql = "SELECT * FROM kdw_tbl_song_menu_event_statics where customerid=%s"
            cursor.execute(sql, cid)
            doc = {}
            doc['userid'] = cid
            doc['songsheet'] = []
            for line in cursor:
                songinfo = {}
                songinfo['songID'] = line.get("songId").encode("utf-8")
                songinfo['songTime'] = datetime.datetime.strptime(str(line.get("updateDate")), '%Y-%m-%d')
                doc['songsheet'].append(songinfo)
            docs.append(doc)
            print(doc.get("userid"))
            mgUserSongSheet.insert_one(doc)
        # mgUserSongSheet.insert_many(docs)

finally:
    t2 = datetime.datetime.now()
    print (t1, t2)
    mgClient.close()
    mysqlConnection.close()
