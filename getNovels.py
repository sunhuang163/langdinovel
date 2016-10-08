# -*- encoding=UTF-8 -*-
#python2
#按照分类获得所有的书籍
import urllib,urllib2,re,random,time
import MySQLdb
from bs4 import BeautifulSoup

def get_book_detail_url():
    index=0
    while (True):
        url = 'http://www.23wx.com/class/8_'+str(index+1)+'.html'
        index += 1
        try:
            conn = MySQLdb.connect(user='root', passwd='123456',
                                   host='localhost', db='langdinovel', charset='utf8')
            cur = conn.cursor()
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

            values = {'name': 'Michael Foord',
                      'location': 'pythontab',
                      'language': 'Python'}
            headers = {'User-Agent': user_agent}
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data, headers)
            html = urllib2.urlopen(req).read()
            print "working"
            soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
            #print "soup----------\n", soup
            list = soup.find_all('tr', bgcolor="#FFFFFF")
            if(len(list)<=0):
                print "over"
                break;
            for tr in list:
                tds = tr.findAll('td')
                novel_name = tds[0].get_text()
                novel_author = tds[2].get_text()
                novel_intro_url = tds[0].find('a')['href']
                novel_catalog_url = tds[1].find('a')['href']
                sql = "insert into novels(novel_navigation,novel_name,novel_author,novel_catalog_url,novel_intro_url)VALUES ('11',%s,%s,%s,%s)"
                bol = cur.execute(sql , (novel_name, novel_author, novel_catalog_url, novel_intro_url))
        except:
            import traceback
            traceback.print_exc()
            cur.close()
            conn.commit()
            conn.close()
            break;
        cur.close()
        conn.commit()
        conn.close()
        if (bol == 1):
            print "success url-", url
        print "sleeping"
        time.sleep(random.random() * 5)
get_book_detail_url()