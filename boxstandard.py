# -*- coding:utf-8 -*-
import pymysql.cursors

import gl
sizedict = {
    '小': '小',
    '中': '中',
    '大': '大',
    '迷你': '迷你'
}
topicdict = {
    '情侣': '情侣',
    '派对': '派对',
    'PARTY': '派对',
    '主题': '主题',
    '商务': '商务'
}
servedict = {
    '普通': '普通',
    '标准': '标准',
    '豪华': '豪华',
    'VIP': 'VIP',
    '旗舰': '豪华',
    '总统': '总统'
}
mysqlConnection = pymysql.connect(host=gl.mysql_host,
                                  port=gl.mysql_port,
                                  user=gl.mysql_user,
                                  password=gl.mysql_password,
                                  db=gl.mysql_db,
                                  charset=gl.mysql_charset,
                                  cursorclass=pymysql.cursors.DictCursor)

try:
    with mysqlConnection.cursor() as cursor:
        sql = 'SELECT * FROM wj_tbl_shoproomsort'
        cursor.execute(sql)
        args = []
        for res in cursor:
            size = ''
            topic = ''
            serve = ''
            roomname = res.get('RoomSortName').encode('utf-8')
            for key in sizedict.keys():
                if roomname.find(key) >= 0:
                    size = sizedict.get(key)
                    break
            for key in topicdict.keys():
                if roomname.find(key) >= 0:
                    topic = topicdict.get(key)
                    break
            for key in servedict.keys():
                if roomname.find(key) >= 0:
                    serve = servedict.get(key)
                    break
            print '%s %s %s %s' %(roomname, size, topic, serve)
            args.append((int(res.get('ShopRoomSortID')), int(res.get('CompanyID')), int(res.get('RoomSortID')),
                         res.get('RoomSortName').encode('utf-8'), size, topic, serve))
        insertsql = '''
            INSERT INTO `roomtrasnfer` (`ShopRoomSortID`, `CompanyID`, `RoomSortID`, `RoomSortName`, `size`, `topic`, `serve`) VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
        for arg in args:
            try:
                print 'insert %s' % str(arg)
                cursor.execute(insertsql, arg)
                mysqlConnection.commit()
            except Exception, e:
                print e
except:
    mysqlConnection.close()