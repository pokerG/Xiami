# -*- coding:utf-8 -*-
import pymysql.cursors

import gl
classdict = {
    '套餐': '套餐',
    '洋酒': '洋酒',
    '红酒': '红酒',
    '啤酒': '啤酒',
    '食品': '小吃',
    '饮料': '饮料',
    '零食': '小吃',
    '水果': '小吃',
    '香烟': '香烟',
    '餐点': '小吃',
    '果盘': '小吃',
    '蛋糕': '小吃',
    '冰淇淋': '小吃',
    '茶': '饮料',
    '小炒': '小吃',
    '果汁': '饮料',
    '小碟': '小吃',
    '鸡尾酒': '洋酒',
    '开水': '饮料',
    '水吧': '饮料',
    '厨房': '厨房',
    '爆米花': '小吃',
    '主食': '小吃',
    '软饮': '饮料',
    '汤': '饮料',
    '凉拌': '小吃',
    '泡椒': '小吃',
    '椒盐': '小吃',
    '特色菜': '小吃',
    '美食': '小吃',
    '水煮': '小吃',
    '卤味': '小吃'
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
        sql = 'SELECT * FROM wj_tbl_shopmaterialsort'
        cursor.execute(sql)
        args = []
        for res in cursor:
            materialclass = ''
            materialname = res.get('MaterialSortName').encode('utf-8')
            for key in classdict.keys():
                if materialname.find(key) >= 0:
                    materialclass = classdict.get(key)
                    break
            if materialclass == '':
                materialclass = '其他'
            print '%s %s' %(materialname, materialclass)
            args.append((int(res.get('ShopMaterialSortID')), int(res.get('CompanyID')), int(res.get('SerialNumber')), int(res.get('MaterialSortID')),
                         res.get('MaterialSortName').encode('utf-8'), materialclass))
        insertsql = '''
            INSERT INTO `materialtrasnfer` (`ShopMaterialSortID`, `CompanyID`, `SerialNumber`, `MaterialSortID`, `MaterialSortName`, `MaterialClass`) VALUES (%s, %s, %s, %s, %s, %s)
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