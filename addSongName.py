# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
import logging
import datetime

import gl

mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgUserSongSheet = mgClient.Xiami.UserSongSheet

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='addSongName.log',
                    filemode='w')

mysqlConnection = pymysql.connect(host=gl.mysql_host,
                                  port=gl.mysql_port,
                                  user=gl.mysql_user,
                                  password=gl.mysql_password,
                                  db=gl.mysql_db,
                                  charset=gl.mysql_charset,
                                  cursorclass=pymysql.cursors.DictCursor)

try:
    with mysqlConnection.cursor() as cursor:
        for document in mgUserSongSheet.find():
            print document.get('_id')
            songsheet = document.get('songsheet')
            sql = 'SELECT * FROM kdw_tbl_song where SongID=%s'
            newsongsheet = []
            for songinfo in songsheet:
                newsonginfo = {}
                cursor.execute(sql, songinfo.get('songID'))
                result = cursor.fetchone()
                if result == None:
                    debuginfo = '%s id  %s song dont found' % (document.get('_id'), songinfo.get('songID'))
                    logging.debug(debuginfo)
                    continue
                songname = result.get('SongName').encode("utf-8")
                newsonginfo['songID'] = songinfo.get('songID')
                newsonginfo['songName'] = songname
                newsonginfo['songTime'] = songinfo.get('songTime')
                newsongsheet.append(newsonginfo)
            mgUserSongSheet.update_one({"_id": document.get('_id')},
                                 {"$set": {"songsheet": newsongsheet}})

finally:
    mgClient.close()
    mysqlConnection.close()


