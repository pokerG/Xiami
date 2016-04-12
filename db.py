# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
from HTMLParser import HTMLParser
import datetime
import logging
import sys

import gl

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.found = False
        self.releasetime = ''

    def refresh(self):
        self.found = False
        self.releasetime = ''

    def handle_data(self, data):
        if self.found:
            self.found = False
            self.releasetime = data
        if data.find('发行时间') >= 0:
            self.found = True


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='db.log',
                    filemode='w')

reload(sys)
sys.setdefaultencoding('utf-8')
hp = MyHTMLParser()
mgClient = pymongo.MongoClient(gl.mg_host, gl.mg_port)
mgExtract = mgClient.Xiami.ExtractData
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
        sql = 'SELECT * FROM kdw_tbl_song'
        cursor.execute(sql)
        num = 0
        n = 0
        args = []
        for res in cursor:
            num += 1
            docs = mgExtract.find({'$or': [{'music_title': res.get('SongName')}, {'music_alias': res.get('SongName')}]})
            releasetime = datetime.datetime.max
            for doc in docs:
                try:
                    # temptime = datetime.datetime.strptime(doc.get('album_info').get('发行时间'), '%Y年%m月%d日')
                    # 中文作为key 用get方法好像不行？
                    for tuple in doc.get('album_info').items():
                        if tuple[0] == '发行时间':
                            temptime = datetime.datetime.strptime(tuple[1], '%Y年%m月%d日')
                    if doc.get('singer_title').find(res.get('songsterName')) >= 0 \
                        or doc.get('singer_alias').find(res.get('songsterName')) >= 0 \
                        or res.get('songsterName').find(doc.get('singer_title')) >= 0 \
                        or res.get('songsterName').find(doc.get('singer_alias')) >= 0:
                        releasetime = temptime
                        break
                    releasetime = temptime if temptime < releasetime else releasetime
                except Exception, e:
                    print '%s     %s' % (str(e), str(doc))
                    logging.debug(str(e) + '   ' + str(doc))
                    continue
            if releasetime != datetime.datetime.max:
                print '%s %s %s %s' % (res.get("SongID").encode('utf-8'), res.get('SongName').encode('utf-8'),
                                       res.get('songsterName').encode('utf-8'), releasetime.date())
                args.append((res.get('SongID').encode('utf-8'), res.get('SongName').encode('utf-8'),
                                     res.get('songsterName').encode('utf-8'), releasetime.date()))
                n += 1

        print(num)
        print(n)
        insertsql = '''
            INSERT INTO `song_info` (`SongID`, `SongName`, `songsterName`, `releaseTime`) VALUES (%s, %s, %s, %s)
            '''
        for arg in args:
            try:
                print 'insert %s' % arg
                cursor.execute(insertsql, arg)
                mysqlConnection.commit()
            except Exception, e:
                logging.debug(str(e) + '             ' + str(arg))
                continue
        # cursor.executemany(insertsql, args)
        # print(result.get('id'))
    # mysqlConnection.commit()
except:
    hp.close()
    mgClient.close()
    mysqlConnection.close()

