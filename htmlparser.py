# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.found = False
        self.td = False
        self.releasetime = ""




    def handle_data(self, data):
        if self.found:
            self.found = False
            self.releasetime = data
        if data.find("发行时间") >= 0:
            self.found = True



if __name__ == "__main__":
    html_code = """
    <table>\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" width=\"64\" valign=\"top\">艺人：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href=\"/artist/2581\" title=\"Timi Zhuo\">卓依婷</a>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" valign=\"top\">语种：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\">国语</td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" valign=\"top\">唱片公司：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\"><a href=\"/search?key=%E5%8C%97%E4%BA%AC%E5%8C%97%E5%BD%B1\" title=\"搜索北京北影\" target=\"_blank\">北京北影</a></td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" valign=\"top\">发行时间：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\">2005年01月01日</td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" valign=\"top\">专辑类别：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\">录音室专辑</td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>
    """
    album_info = html_code
    album_info = album_info.replace('\r', '')
    album_info = album_info.replace('\n', '')
    album_info = album_info.replace('\t', '')
    hp = MyHTMLParser()
    hp.feed(album_info)
    print hp.releasetime
    hp.close()
