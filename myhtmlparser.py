# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser
import sys

class countHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.sharecount = 0
        self.commentcount = 0
        self.fanscount = 0
        self.collectcount = 0
        self.temp = 0

    def refresh(self):
        self.sharecount = 0
        self.commentcount = 0
        self.fanscount = 0
        self.collectcount = 0
        self.temp = 0

    def handle_data(self, data):
        if data.isdigit():
            self.temp = int(data)
        elif data == "分享":
            self.sharecount = self.temp
        elif data == "粉丝":
            self.fanscount = self.temp
        elif data == "收藏":
            self.collectcount = self.temp
        elif data == "评论":
            self.commentcount = self.temp


class tagsHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tags = []
        self.a = False

    def refresh(self):
        HTMLParser.reset(self)
        self.tags = []
        self.a = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.a = True

    def handle_data(self, data):
        if self.a:
            self.tags.append(data)
            self.a = False


class infoHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.pair = True
        self.record = False
        self.temp = ''
        self.info = {}

    def refresh(self):
        self.pair = True
        self.record = False
        self.temp = ''
        self.info = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for (var, value) in attrs:
                if var == 'class' and value == 'record':
                    self.record = True
                    return
        if self.record and tag == 'a':
            for (var, value) in attrs:
                if var == 'class' and value == 'more':
                    self.info["档案"] = self.info["档案"].replace('\t','')
                    self.info["档案"] = self.info["档案"].replace('\n', '')
                    self.info["档案"] = self.info["档案"].replace('\r', '')
                    self.record = False
                    self.pair = True
                    return

    def handle_data(self, data):
        if self.record:
            if '档案' in self.info:
                self.info['档案'] = self.info['档案'] + data
            else:
                self.info['档案'] = data
            return
        if not (data.find('\n') >= 0 or data.find('\t') >= 0):
            if self.pair:
                self.temp = data[:data.find('：')] if data.find('：') >= 0 else data
                self.pair = False
            else:
                self.info[self.temp] = data
                self.pair = True

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    html_code = """
    <table id=\"albums_info\" summary=\"song related album info\">\r\n                    <tr>\r\n                      <td class=\"item\" valign=\"top\">所属专辑：</td>\r\n                      <td valign=\"top\"><div style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\"><a href=\"/album/1371103908\" title=\"티아라 &amp; 더 씨야 &amp; 파이브돌스 &amp; 스피드\">Tears Of Mind</a></div></td>\r\n                    </tr>\r\n                    <tr>\r\n                      <td class=\"item\" width=\"64\" valign=\"top\">演唱者：</td>\r\n                      <td valign=\"top\"><div style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\"><a href=\"http://www.xiami.com/search/find?artist=T-ara\" title=\"T-ara\">T-ara</a>; <a href=\"http://www.xiami.com/search/find?artist=The+Seeya\" title=\"The Seeya\">The Seeya</a>; <a href=\"http://www.xiami.com/search/find?artist=5dolls\" title=\"5dolls\">5dolls</a>; <a href=\"http://www.xiami.com/search/find?artist=SPEED\" title=\"SPEED\">SPEED</a>                      </div></td>\r\n                    </tr>\r\n                                        <tr>\r\n                      <td class=\"item\" valign=\"top\">作词：</td>\r\n                      <td valign=\"top\"><div title=\"이단옆차기\" style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\">이단옆차기</div></td>\r\n                    </tr>\r\n                                                            <tr>\r\n                      <td class=\"item\" valign=\"top\">作曲：</td>\r\n                      <td valign=\"top\"><div title=\"이단옆차기.조영수\" style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\">이단옆차기.조영수</div></td>\r\n                    </tr>\r\n                                                            <tr>\r\n                      <td class=\"item\" valign=\"top\">编曲：</td>\r\n                      <td valign=\"top\"><div title=\"이단옆차기\" style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\">이단옆차기</div></td>\r\n                    </tr>\r\n                                      </table>
    """

    hp = infoHTMLParser()
    hp.feed(html_code)
    for var in hp.info:
        print var, hp.info.get(var)
    hp.close()
