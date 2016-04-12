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
        self.tr = False
        self.record = False
        self.temp = ''
        self.info = {}

    def refresh(self):
        self.pair = True
        self.record = False
        self.temp = ''
        self.info = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.tr = True
        if tag == 'div':
            for (var, value) in attrs:
                if var == 'class' and value == 'record':
                    self.record = True
                    return
        if self.record and tag == 'a':
            for (var, value) in attrs:
                if var == 'class' and value == 'more':
                    self.info["档案"] = self.info["档案"].replace('\t', '')
                    self.info["档案"] = self.info["档案"].replace('\n', '')
                    self.info["档案"] = self.info["档案"].replace('\r', '')
                    self.record = False
                    self.tr = False
                    self.pair = True
                    return

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.tr = False
            self.pair = True
    def handle_data(self, data):
        if self.record:
            if '档案' in self.info:
                self.info['档案'] = self.info['档案'] + data
            else:
                self.info['档案'] = data
            return
        if self.tr:
            if not(data.find('\n') >= 0 or data.find('\t') >=0 or data.find('\r')>=0):
                if self.pair:
                    self.temp = data[:data.find('：')] if data.find('：') >=0 else data
                    self.pair = False
                else:
                    if self.temp in self.info:
                        self.info[self.temp] += ' ' + data
                    else:
                        self.info[self.temp] = data

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    html_code = """
    <table id=\"albums_info\" summary=\"song related album info\">\r\n                    <tr>\r\n                      <td class=\"item\" valign=\"top\">所属专辑：</td>\r\n                      <td valign=\"top\"><div style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\"><a href=\"/album/1371103908\" title=\"티아라 &amp; 더 씨야 &amp; 파이브돌스 &amp; 스피드\">Tears Of Mind</a></div></td>\r\n                    </tr>\r\n                    <tr>\r\n                      <td class=\"item\" width=\"64\" valign=\"top\">演唱者：</td>\r\n                      <td valign=\"top\"><div style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\"><a href=\"http://www.xiami.com/search/find?artist=T-ara\" title=\"T-ara\">T-ara</a>; <a href=\"http://www.xiami.com/search/find?artist=The+Seeya\" title=\"The Seeya\">The Seeya</a>; <a href=\"http://www.xiami.com/search/find?artist=5dolls\" title=\"5dolls\">5dolls</a>; <a href=\"http://www.xiami.com/search/find?artist=SPEED\" title=\"SPEED\">SPEED</a>                      </div></td>\r\n                    </tr>\r\n                                        <tr>\r\n                      <td class=\"item\" valign=\"top\">作词：</td>\r\n                      <td valign=\"top\"><div title=\"이단옆차기\" style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\">이단옆차기</div></td>\r\n                    </tr>\r\n                                                            <tr>\r\n                      <td class=\"item\" valign=\"top\">作曲：</td>\r\n                      <td valign=\"top\"><div title=\"이단옆차기.조영수\" style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\">이단옆차기.조영수</div></td>\r\n                    </tr>\r\n                                                            <tr>\r\n                      <td class=\"item\" valign=\"top\">编曲：</td>\r\n                      <td valign=\"top\"><div title=\"이단옆차기\" style=\"white-space:nowrap; width:140px; overflow:hidden; text-overflow:ellipsis;\">이단옆차기</div></td>\r\n                    </tr>\r\n                                      </table>
    """

    singer_info = """
    <table>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" width=\"56\" valign=\"top\">地区：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\">Taiwan 台湾</td>\r\n\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" width=\"56\" valign=\"top\">风格：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\">\r\n\t\t\t\t\t\t\t\t\t\t<a href=\"/genre/detail/sid/1541\" rel=\"nofollow\">国语流行 Mandarin Pop</a></td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td class=\"item\" width=\"56\" valign=\"top\">档案：</td>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\">\r\n\t\t\t\t\t\t\t\t\t\t<div class=\"record\">\r\n\t\t\t\t\t\t\t\t\t\t邓丽君（Teresa Teng，1953年1月29日－1995年5月8日）是一位在亚洲地区和全球华人社会极具影响力的台湾歌唱家，亦是20世纪后半叶最富盛名的日本歌坛巨星之一。她的歌曲在华人社会广泛的知名度和经久不衰的传唱度为其赢得了“十亿个掌声”的美誉，“有华人的地方就有邓丽君的歌声”，被日本艺能界尊为“亚洲歌唱女王”。其生前演艺足迹遍及台湾、中国大陆、香港、日本、美国、东南亚等国家和地区，发表国语、日语、英语、粤语、闽南语、印尼语歌曲1000余首，对华语乐坛尤其是中国流行乐坛的启蒙与发展产生深远影响，也为开创日本演歌流行化新曲风和促进亚洲流行音乐文化的交流做出了重要贡献。时至今日，仍有无数歌手翻唱她的经典歌曲向其致敬，被誉为华语流行乐坛永恒的文化符号。<br>1995年邓丽君因哮喘去世于泰国清迈，国葬于台北金宝山筠园。<br>小档案<br>原名：邓丽筠<br>日文名：テレサ·テン<br>昵称：丽君、小邓<br>称号：天才歌手、学生情人、永远的邓丽君<br>性格：亲切、诚实、天真、坚强<br>语言：国语、粤语、闽南话、山东话、英语、日语、法语、马来西亚语等<br>生日：1月29日 周四 壬辰年腊月十五日<br>星座：水瓶<br>血型：O<br>属相：龙<br>身高：1.67<br>体重：47<br>形体：826091<br>优点：腿形修长<br>烦恼：担心发胖<br>职业：歌手<br>签约公司：宇宙、丽风、宝丽多、宝丽金<br>出道年代：1967年 9月·台湾 1974年 3月·日本<br>籍贯：河北大名<br>出生地：台湾云林<br>家庭成员：父母和兄弟<br>喜欢颜色：紫色、桃色<br>喜欢跳舞：DISCO<br>喜欢运动：网球<br>喜欢服装：网球装，牛仔服<br>喜欢香水：青草香型<br>喜欢饰物：项链、戒指<br>喜欢珠宝：钻石<br>喜欢玩具：洋娃娃<br>喜欢收藏：自己的新闻剪报<br>最贴身首饰：左手的玉镯<br>喜欢动物：小松鼠（小动物）海豚（大动物）<br>喜欢花卉：玫瑰花<br>爱好趣味：听音乐<br>休闲方式：一个人冲杯茶听音乐<br>喜欢书籍：齐瓦哥医生<br>最大愿望：念书<br>儿时理想：当护士<br>慈善关怀：老人和儿童<br>喜欢蔬菜：空心菜<br>拿手菜肴：炒空心菜<br>喜欢口味：辣的食物<br>喜欢食物：猪脚<br>喜欢饮料：香吉士<br>最苦的食物：苦瓜<br>最甜的食物：羊羹<br>喜欢建筑：小木屋<br>喜欢城市：香港、金门<br>最难忘风景：槟城<br>最难忘演出：马来西亚<br>最喜欢旅馆：印尼、新加坡旅馆<br>最喜欢地区：新加坡、金门<br>最难忘的事：第一次上台视群星会忘词<br>流泪唱的歌：再见，我的爱人<br>喜欢的老师：初中级任老师<br>最信任的人：爸妈<br>最难忘的人：小学同学<br>撒娇的对象：哥哥<br>生气的对象：经理人<br>喜欢电影：乱世佳人<br>喜欢影星：劳伯瑞福<br>喜欢歌星：戴安娜罗丝<br>最欣赏歌星：凤飞飞<br>最崇拜人物：南丁格尔<br>最羡慕美人：西施、林黛玉<br>最怕的人：蛮横无理的人<br>最怕的歌：肉麻的歌<br>最怕动物：老虎、蛇<br>最怕电影：恐怖片<br>最怕食物：鳗鱼<br>最怕衣服：没有<br>最怕问题：问年龄<br>最头痛的事：背书<br>最喜欢打听：男歌迷的年龄及婚否<br>最喜欢手势：V字手势<br>最长来信：十五页<br>最短写信：六十个字<br>初恋年龄：八岁或七岁<br>最初赚钱：十二岁<br>最大财富：十亿个掌声 永远的怀恋<br>大事记<br>1953 1月29日出生于台湾省云林县褒忠乡田洋村<br>1958 至屏东市仙宫戏院附近学芭蕾舞<br>1963 参加中华电台黄梅调歌曲比赛以《访英台》获得冠军<br>1964 代表学校参加全县国语朗读比赛，获得第一名<br>1966 参加金马奖唱片公司歌唱比赛，以《采红菱》夺得冠军。<br>1967 自金陵女中休学加盟宇宙唱片公司，九月推出第一张唱片，正式以歌唱为职业<br>1969 演出第一部电影《谢谢总经理》<br>演唱中视开播首档连续剧《晶晶》主题曲及主持中视《每日一星》节目<br>应新加坡总统夫人邀请首度出国赴约做慈善义演<br>1970 获白花油义卖“慈善皇后”荣誉<br>随“凯声综艺团”到香港表演<br>在港拍电影《歌迷小姐》<br>1973 与日本“宝丽多”机构签约赴日发展<br>到香港演唱于“香港歌剧院”、“汉宫”及“珠城”，后前赴越南演唱<br>1974 以《空港》一曲当选1974年“最佳新人歌星赏”<br>1977 成为“香港第一届金唱片颁奖礼”一位金唱片得主<br>1978 个人大碟《邓丽君GREATEST HITS》及《岛国之情歌--第三集》同时获香港第三届金唱片奖<br>于日本以《东京夜景》获得“正顽张中赏”<br>1979 “香港第四届金唱片颁奖礼”上，同时有三张大碟获白金唱片奖，另有两张大碟获金唱片奖<br>赴美进修日文、英文、生物及数学，四月首次在加拿大温哥华举行演唱会<br>1980 荣获台湾金钟奖“最佳女歌星奖”<br>在美国纽约林肯中心、洛杉矶音乐中心登台<br>邓丽君身在美国，然而其歌声却响遍神州大地，大江南北的民众为邓丽君歌声而醉倒。据悉，连小平同志也甚为欣赏邓丽君独<br>特的演绎方式<br>在香港推出第一张粤语大碟--《势不两立》，瞬即达到白金唱片数字<br>第四度踏足“利舞台”，举行一连七场个人演唱会<br>十月返台于国父纪念馆义唱，门票收入全数捐作自强爱国基金<br>年底赴东南亚作巡回表演<br>1981 台新闻局颁发“爱国艺人”奖座，与李季准主持金钟奖典礼<br>在香港利舞台创下个人演唱会场次最多之记录<br>六月于台湾义演，“台视”播出长达一百二十分钟《君在前哨》特别节目<br>参加“香港第五届金唱片颁奖礼”，她所灌五张个人大碟同时获白金唱片，勇破历届金唱片记录<br>1982 于香港举办个人演唱会，推出《邓丽君演唱会》双唱片，面世即双双成为白金唱片<br>1983 赴拉斯维加斯“凯撒皇宫”演唱，是首位在此签约演唱的华籍女歌手<br>当选“十大杰出女青年”<br>推出广东大碟《漫步人生路》，唱至街知巷闻<br>1984 在东南亚各地举办十五周年巡回演唱会<br>重返日本推出《偿还》专辑，立即打入日本唱片流行榜，停留榜内接近一年，刷新日本乐坛历史记录。邓丽君也因此获得无数<br>奖项，其中包括“年度有线大赏”、“最受欢迎歌曲赏”，更被提名角逐“日本唱片大赏”之“最优秀歌唱赏”。其卓越成<br>就，为中华民族添上一抹缤纷艳丽的光彩<br>1985 在日本凭借新歌《爱人》连续十四周蝉联日本广播“点唱流行榜”冠军，并再夺“有线放送大赏”，同时在日本乐坛创<br>下两项历史记录<br>《爱人》一曲不费吹灰之力便入选日本“第36回红白歌合战”<br>首次参与电视剧演出，《爱人》一曲更成为该剧主题曲<br>八月返台与张菲主持“反盗录、反仿冒”义演晚会。十二月在日本NHK大会堂举行演唱会<br>1986 主持台视春节特别节目“与君同乐”<br>单曲《任时光从身边流逝》蝉联日本年度有线电视大赏<br>再度以大热门姿态顺利入选日本“第37回红白歌合战”<br>1987 继续穿梭于香港、台湾、美加及法国等地，但已处于半退休状态，除参与慈善演出外，甚少于公众场合露面<br>赴纽约参加“国际公益金”义演<br>出席日本“第38回红白歌合战”<br>1988 名作词家慎芝女士过逝专程返台吊唁<br>1989 香港“亚洲电视”于农历年初二晚直播烟花汇演，邓丽君应邀出席，并演唱一曲《漫步人生路》<br>1990 应邀出席“无线电视”直播之慈善节目，作表演嘉宾<br>1991 赴港为“爱心献华东”赈灾筹款，作慈善表演嘉宾<br>1992 推出《难忘的TERESA TENG》专集<br>1993 三月赴港作“亚洲电视”TALK SHOW“龙门阵”嘉宾<br>1994 参加华视庆祝黄埔军校建校七十周年所举办的“永远的黄埔”晚会，为最后一次在台湾之公开演出<br>于日本推出《夜来香》唱片<br>1995 五月八日因气喘病发猝逝泰国清迈，享年四十二岁，五月二十八日在国人及全球华人目送之下长眠金宝山“筠园”\r\n\t\t\t\t\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t\t\t\t\t<a href=\"/artist/profile-1483\" class=\"more\">(更多)</a>\t\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t</table>
    """

    hp = infoHTMLParser()
    hp.feed(html_code)
    for var in hp.info:
        print var, hp.info.get(var)
    hp.close()
