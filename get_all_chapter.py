# -*- encoding=UTF-8 -*-
#下载书籍的所有章节到mysql
import urllib,urllib2,re,time,random,MySQLdb
from bs4 import BeautifulSoup
from header import *
def start_read(novel_name,novel_author):
    novel_info=get_novel_id_DB(novel_name,novel_author)
    if(novel_info=='nonono'):
        print "sorry can't find the novel"
        return
    req_header = getHeader()
    req_timeout = 20
    req = urllib2.Request(novel_info[1], None, req_header)
    resp = urllib2.urlopen(req, None, req_timeout)
    html = resp.read()
    soup=BeautifulSoup(html,'html.parser', from_encoding='gbk')
    firstCap=soup.find('table',id="at").find('a')
    url_temp = novel_info[1] + firstCap['href']
    index=0
    while(True):
        index+=1
        url_next=get_chapter_text(url_temp,novel_info,index)
        if((not url_next==None) and '/html/' in url_next):
            url_next=url_next[len(novel_info[1])-len(host):]
        if (url_next==None):
            print 'ok! read sucess'
            break
        url_temp = novel_info[1]+url_next
        print "sleeping ZZZ"
        time.sleep(random.random() * 2)

def get_novel_id_DB(novel_name,novel_author):
    novel_name=novel_name.strip()
    novel_author=novel_author.strip()
    conn = MySQLdb.connect(user='root', passwd='123456',
                           host='localhost', db='langdinovel', charset='utf8')
    cur = conn.cursor()
    sql = "select id,novel_catalog_url,novel_name,novel_author from novels WHERE novel_name=%s and novel_author=%s"
    bol = cur.execute(sql, (novel_name,novel_author))
    if(1==bol):
        novel = cur.fetchone()
        return novel
    else:
        return 'nonono'

def get_chapter_text(url,novel_info,index):
    try:
        while (True):
            time.sleep(random.random() * 2)
            print 'working>>>', novel_info[2], novel_info[3],index, 'cap:', 'url:', url
            req_header = getHeader()
            req = urllib2.Request(url, None, req_header)
            resp = urllib2.urlopen(req, None)
            html = resp.read()
            if(not resp.getcode()==200):
                print 'time out！ repeat', url
                continue
            soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
            try:
                ispage=soup.find('title').get_text()
                if(novel_info[2] in ispage):
                    break
            except:
                print 'repeat',url
        content = soup.find('dd', id="contents")
        title = soup.find('h1')
        put_text_DB(novel_info[0], title.get_text(), content.get_text())
        next_page = soup.find_all('a', href=re.compile("[0-9]+.html$"))
        for next in next_page:
            if (next.get_text() in '下一页'):
                return next['href']
    except:
        print 'error cap:',url
        import traceback
        traceback.print_exc()
        exit(-1)
def put_text_DB(novel_id,catalog_name,catalog_content):
    conn = MySQLdb.connect(user='root', passwd='123456',
                           host='localhost', db='langdinovel', charset='utf8')
    cur = conn.cursor()
    sql = "insert into catalogs(novel_id,catalog_name,catalog_content) VALUES (%s,%s,%s)"
    bol = cur.execute(sql, (novel_id,catalog_name,catalog_content))
    if(bol==0):
        print 'DB error! exit'
        exit(-1)
    cur.close()
    conn.commit()
    conn.close()
host='http://www.23wx.com'
start_read('儒道至圣','永恒之火')
