# coding:utf-8
# author: CG
# date: 2/9/2018
# Python 大法好！

from urllib import request
import re
import os
import shutil

girlscates = [
    'http://www.meizitu.com/a/pure.html',
    'http://www.meizitu.com/a/cute.html',
    'http://www.meizitu.com/a/sexy.html',
    'http://www.meizitu.com/a/fuli.html',
    'http://www.meizitu.com/a/legs.html',
    'http://www.meizitu.com/a/rixi.html',
    'http://www.meizitu.com/a/yundong.html',
    'http://www.meizitu.com/tag/mote_6_1.html',
    'http://www.meizitu.com/tag/keai_64_1.html',
    'http://www.meizitu.com/tag/qizhi_53_1.html',
    'http://www.meizitu.com/tag/banluo_5_1.html',
    'http://www.meizitu.com/tag/nvshen_460_1.html',
    'http://www.meizitu.com/tag/quanluo_4_1.html',
    'http://www.meizitu.com/tag/chengshu_487_1.html'
]
catestring = ['颜值控', '萌妹', '性感', '福利', '美腿', '日系', '运动', '模特', '可爱', '气质', '半身棵体',
              '女神', '全身棵体', '成熟']


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
        html = cls.openurl(girlscates[index - 1])
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
            # print(html)
            imgurlstr = re.search('(?<="picture">)(.|\n)*?(?=</div>)', html, re.M).group()
            imgurlstrs = imgurlstr.split("<br />")
            imgurls = []
            try:
                for imgurlstring in imgurlstrs:
                    imgurls.append(imgurlstring.split("src")[1].split("\"")[1])
                # imgurls = [i.split("src")[1].split("\"")[1] for i in imgurlstrs]  不能用！ 因为最后一个元素会导致indexoutofbound导致列表推导式生成空数组
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
                    print("\n" * 20)
                    print("爬取中。。。" + '已爬取：' + str(cls.number) + '/' + '共计：' + str(cls.count))
                    if cls.count <= cls.number:
                        print("爬取完成")
                        os._exit(0)
            except:
                pass

        pass

    @classmethod
    def run(cls):
        str1 = ''
        info = '请选择爬取的图片类型（输入数字编号）：\n'
        for a in range(len(catestring)):
            info = info + str(a+1) + '.' + catestring[a] + '\n'
        while (not str1.isnumeric() or not 0 < int(str1) < 15 or not 0 < cls.count):
            str1 = input(info)
            cls.count = int(input("想要几张？\n"))
        cls.cate = catestring[int(str1) - 1]
        cls.getmainpage(int(str1))


c = Crawler()
c.run()
