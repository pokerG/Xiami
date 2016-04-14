# -*- coding:utf-8 -*-
import pymysql.cursors
import datetime
import logging
import sys

import gl

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='fileimport.log',
                    filemode='w')

mysqlConnection = pymysql.connect(host=gl.mysql_host,
                                  port=gl.mysql_port,
                                  user=gl.mysql_user,
                                  password=gl.mysql_password,
                                  db=gl.mysql_db,
                                  charset=gl.mysql_charset,
                                  cursorclass=pymysql.cursors.DictCursor)

try:
    insertsql = '''
        INSERT INTO `song_info` (`SongID`, `SongName`, `songsterName`, `releaseTime`) VALUES (%s, %s, %s, %s)
        '''
    with mysqlConnection.cursor() as cursor:
        with open('songreleasetime.data', 'r') as f:
            for line in f:
                line = line[:-1]
                arg = map(str, line.split('@'))
                try:
                    print 'insert %s' % str(arg)
                    cursor.execute(insertsql, arg)
                    mysqlConnection.commit()
                except Exception, e:
                    logging.debug(str(e) + '             ' + str(arg))
                    continue

except:
    mysqlConnection.close()
