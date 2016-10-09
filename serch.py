# -*- encoding=UTF-8 -*-
#输入书籍名字，获得最新章节url
import urllib,urllib2,time
from bs4 import BeautifulSoup
from header import *
class serchNovel:
    keyword=''
    introduction=''
    author = ''
    word_number=''
    click_number=''
    update_status=''

    def __init__(self,keyword):
        self.keyword=keyword.strip()
    def __del__(self):
        print '__del__ ok'
    def urlcode(self):
        key = self.keyword
        key = key.decode('utf8', 'replace')
        print urllib.quote(key.encode('gbk', 'replace'))
        return urllib.quote(key.encode('gbk', 'replace'))
    def serch(self):
        url='http://www.23wx.com/modules/article/search.php'
        index=1
        while(True):
            if(index==10):
                print "failed can't find the book"
                return 'nonono'
            print 'working>> serch time',index,'most time 10'
            index+=1
            time.sleep(random.random() * 5)
            req_header = getHeader()
            data = {'searchtype':'articlename','searchkey':'11'}
            data['searchkey']=self.keyword.encode('gbk')
            req = urllib2.Request(url, None, req_header)
            resp=urllib2.urlopen(
                req,
                data=urllib.urlencode(data)
            )
            html = resp.read()
            soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
            novel_div=soup.find('dl',id="content").find('div',class_='fl')
            href=novel_div.find('a',class_="hst")['href']
            if (not resp.getcode() == 200):
                print 'time out！ repeat', url
                continue
            try:
                ispage = soup.find('title').get_text()
                if ('顶点小说' in ispage):
                    return href
            except:
                print 'errorpage repeat', url
