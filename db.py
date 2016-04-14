# -*- coding:utf-8 -*-
import pymysql.cursors
import pymongo
from HTMLParser import HTMLParser
import datetime
import logging
import sys

import gl

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='db.log',
                    filemode='w')

reload(sys)
sys.setdefaultencoding('utf-8')
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
                            break
                    # 防止名字缺失引起的匹配
                    n1 = doc.get('singer_title') if doc.get('singer_title') != '' else '!@#$%^&*'
                    n2 = doc.get('singer_alias') if doc.get('singer_alias') != '' else '!@#$%^&*'
                    n3 = res.get('songsterName') if res.get('songsterName') != '' else '!@#$%^&*'
                    if n1.find(n3) >= 0 or n2.find(n3) >= 0 or n3.find(n1) >= 0 or n3.find(n2) >= 0:
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
                with open('songreleasetime.data', 'a') as f:
                    f.write('%s@%s@%s@%s\n' % (res.get("SongID").encode('utf-8'), res.get('SongName').encode('utf-8'),
                                             res.get('songsterName').encode('utf-8'), releasetime.date()))
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
                print 'insert %s' % str(arg)
                cursor.execute(insertsql, arg)
                mysqlConnection.commit()
            except Exception, e:
                logging.debug(str(e) + '             ' + str(arg))
                continue
        # cursor.executemany(insertsql, args)
        # print(result.get('id'))
    # mysqlConnection.commit()
except:
    mgClient.close()
    mysqlConnection.close()

