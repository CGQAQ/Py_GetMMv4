# coding:utf-8
# author: CG
# date: 4/2/2017
# Python 大法好！

from urllib import request
import re
import os
import shutil

girlscates = ['http://www.meizitu.com/a/xinggan.html',
              'http://www.meizitu.com/a/sifang.html',
              'http://www.meizitu.com/a/qingchun.html',
              'http://www.meizitu.com/a/meizi.html',
              'http://www.meizitu.com/a/xiaoqingxin.htm', #end with .htm
              'http://www.meizitu.com/a/nvshen.html',
              'http://www.meizitu.com/a/qizhi.html',
              'http://www.meizitu.com/a/mote.html',
              'http://www.meizitu.com/a/bijini.html',
              'http://www.meizitu.com/a/baobei.html',
              'http://www.meizitu.com/a/luoli.html',
              'http://www.meizitu.com/a/wangluo.html',
              'http://www.meizitu.com/a/rihan.html',
              'http://www.meizitu.com/a/oumei.html']
catestring = ['性感','浴室','私房','美腿','清纯','甜美','治愈系','萌妹子','小清新','女神','气质美女',
              '嫩模','车模','比基尼','足球','萝莉','90后','日韩','欧美']

class Crawler:
    cate = ''
    count = 0
    number = 0
    @classmethod
    def openurl(cls, url):
        """
        customize fetching html code method
        :param url: 
        :return: html code string
        """
        res = request.urlopen(url)
        html = res.read().decode('gb2312', 'ignore')
        return html

    @classmethod
    def getmainpage(cls, index):
        """
        
        :param index: number of girls category
        :return: none
        """
        html = cls.openurl(girlscates[index-1])
        while 1:
            nextpageurl = cls.getsubpage(html)
            if nextpageurl == '':
                break
            html = cls.openurl(nextpageurl)
        pass

    @classmethod
    def getsubpage(cls, html):
        """
        :param html : Html code which is need analysis
        :return: none
        """
        # next page url regex  (?<=href=').*?(?='>下一页)
        # Detailed page regex  (?<=class="tit"><a href=").*?(?=")
        try:
            nextpageurl = re.search("(?<=href=').*?(?='>下一页)", html, re.M).group()
        except:
            nextpageurl = ''

        details = re.findall('(?<=class="tit"><a href=").*?(?=")', html, re.M)


        cls.fetchimg(details)
        return nextpageurl

    @classmethod
    def fetchimg(cls, details):
        """
        :param details: details page url list
        :param nextpage: next page url
        :return: none
        """

        if not os.path.exists("./MM/"):
            os.mkdir('./MM/')
        if not os.path.exists("./MM/" + cls.cate):
            os.mkdir("./MM/" + cls.cate)
        if os.listdir("./MM/" + cls.cate):
            shutil.rmtree("./MM/" + cls.cate)
            os.mkdir("./MM/")
            os.mkdir("./MM/" + cls.cate)
        for url in details:
            html = cls.openurl(url)
            #print(html)
            imgurlstr = re.search('(?<="picture">)(.|\n)*?(?=</div>)', html, re.M).group()
            imgurlstrs = imgurlstr.split("<br />")
            imgurls = []
            try:
                for imgurlstring in imgurlstrs:
                    imgurls.append(imgurlstring.split("src")[1].split("\"")[1])
            except:
                pass
            try:
                for imgurl in imgurls:
                    req = request.Request(imgurl, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'})
                    res = request.urlopen(req)
                    with open("./MM/" + cls.cate + '/' + imgurl.split('uploads/')[-1].replace('/', '_'), 'wb') as f:
                        f.write(res.read())
                    cls.number += 1
                    print("\n"*20)
                    print("爬取中。。。" + '已爬取：'+str(cls.number)+'/'+'共计：'+str(cls.count))
                    if cls.count <= cls.number:
                        print("爬取完成")
                        os._exit(0)
            except:
                pass

        pass

    @classmethod
    def run(cls):
        str = ''
        while(not str.isnumeric() or not 0<int(str)<20 or not 0 < cls.count):
            str = input('请选择爬取的图片类型（输入数字编号）：\n'
                        '1.性感\n'
                        '2.浴室\n'
                        '3.私房\n'
                        '4.美腿\n'
                        '5.清纯\n'
                        '6.甜美\n'
                        '7.治愈系\n'
                        '8.萌妹子\n'
                        '9.小清新\n'
                        '10.女神\n'
                        '11.气质美女\n'
                        '12.嫩模\n'
                        '13.车模\n'
                        '14.比基尼\n'
                        '15.足球宝贝\n'
                        '16.萝莉\n'
                        '17.90后\n'
                        '18.日韩\n'
                        '19.欧美\n')
            cls.count = int(input("想要几张？\n"))
        cls.cate = catestring[int(str)-1]
        if str=='1' or str=='2':
            cls.getmainpage(1)
        elif str=='3' or str=='4':
            cls.getmainpage(2)
        elif str=='5' or str=='6' or str=='7':
            cls.getmainpage(3)
        elif str =='8':
            cls.getmainpage(4)
        elif str=='9':
            cls.getmainpage(5)
        elif str=='10':
            cls.getmainpage(6)
        elif str=='11':
            cls.getmainpage(7)
        elif str=='12' or str=='13':
            cls.getmainpage(8)
        elif str=='14':
            cls.getmainpage(9)
        elif str=='15':
            cls.getmainpage(10)
        elif str=='16':
            cls.getmainpage(11)
        elif str=='17':
            cls.getmainpage(12)
        elif str=='18':
            cls.getmainpage(13)
        elif str=='19':
            cls.getmainpage(14)

c = Crawler()
c.run()