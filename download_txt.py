# -*- encoding=UTF-8 -*-
#下载txt文本文件，可指定开始章节(根据保存mysql方法改编)
from header import *
from serch import *
from bs4 import BeautifulSoup
class download_txt:
    url =''
    novel_name=''
    start_cap=''
    flag=True
    def __init__(self,novelname,start_cap=0):
        ser=serchNovel(novelname)
        self.url=ser.serch()
        if(self.url=='nonono'):
            exit(-1)
        print self.url
        self.novel_name = novelname
        self.start_cap = start_cap
        if(start_cap==0):
            self.flag=False
    def download(self):
        req_header = getHeader()
        req_timeout = 20
        req = urllib2.Request(self.url, None, req_header)
        resp = urllib2.urlopen(req, None, req_timeout)
        html = resp.read()
        soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
        Caplist = soup.find('table', id="at").find_all('a')
        f = open(self.novel_name.decode('utf8')+"_"+str(self.start_cap)+'_PowerByJoy.txt','w')
        index=0
        for cap in Caplist:
            index += 1
            titleq=cap.get_text()
            if(self.flag):
                if(str(self.start_cap) in titleq):
                    self.flag=False
                else:
                    continue
            print 'process :',index,'/',len(Caplist)
            if('更新重要通告' in titleq):
                print self.novel_name,'下载完成！'
                f.close()
                exit(0)
            txt=self.get_conntext(cap,index)
            f.write(titleq)
            f.write('\n')
            f.write(txt.replace('    ','\n'))

    def get_conntext(self,cap,index):
        cap_url=self.url+cap['href']
        while (True):
            time.sleep(random.random() * 4)
            print 'working>>>', cap_url, index, 'cap:'
            req_header = getHeader()
            req = urllib2.Request(cap_url, None, req_header)
            resp = urllib2.urlopen(req, None)
            html = resp.read()
            if (not resp.getcode() == 200):
                print 'time out！ repeat', cap_url
                continue
            soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
            try:
                ispage = soup.find('title').get_text()
                if (self.novel_name in ispage):
                    break
            except:
                print 'repeat', cap_url
        content = soup.find('dd', id="contents")
        return content.get_text()

#使用实例：参数一：小说名，参数二：开始的章节（ps：可以不写，默认重第一章开始，注意：汉字章节编号要写汉字）
#d=download_txt('超品相师','第十一章')
d=download_txt('超品相师',2548)
d.download()
