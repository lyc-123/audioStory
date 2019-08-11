import requests
import urllib
import re
import os
import time
class YsSpider:
    def __init__(self, name):
        self.search_name = name
        self.search_url = "http://www.ting89.com/search.asp?searchword="
        self.home_url = "http://www.ting89.com/books/"
        self.index_pattern = r"""<a href="/books/([0-9]+).html" title="(.+?)" target='_blank'>"""
        self.chapter_pattern=r"""<a href='(/down/\?[^-]+-\d+.html)' target="_blank">(.+?)</a>"""
        self.down_pattern=r"""url=(.*)/(.+?)\.mp3"""
        self.book_id = ''
        self.book_name = ''
        self.Chapter_list = []

    # 返回搜索书目的id
    def searchbook(self):
        file = requests.get(self.search_url + urllib.parse.quote(self.search_name, encoding='gb2312'))
        data = file.content.decode('gbk')
        result = re.findall(self.index_pattern, data)
        if len(result):
            for index, i in enumerate(result):
                print('%d.%s'%(index+1,i[1]))
                # str = input("输入你要下载的书目名称序号: ")
                str = '1'
                self.book_name = result[int(str)-1][1]
                self.book_id = result[int(str)-1][0]
                return self.book_id
            else:
                print('*******没有找到你输入的相关书籍,请更换后重新运行程序*******')
                exit()

    def get_chapter_list(self):#获取各章节list和url
        data = requests.get(self.home_url+self.searchbook()+'.html').content.decode('gbk')
        result = re.findall(self.chapter_pattern, data)
        return result
    def _getAllUrl(self):# 获得所有的章节的下载地址
        chapter_list = self.get_chapter_list()
        chapter = [x[0] for x in chapter_list]
        self.Chapter_list= [x[1] for x in chapter_list]
        _list = [x[1] for x in chapter_list]
        data = requests.get("http://www.ting89.com" + chapter[0]).content.decode('gbk')
        result = re.findall(self.down_pattern, data)
        # return result
        return self.sub_get_url(result[0][0],_list, re.search("^0.*1$", result[0][1]))

    def sub_get_url(self, down_url, _list, down_url_flag):
        url = []
        if down_url_flag:
            xulie = list(range(len(_list)))
            weishu = len(str(xulie[-1]))
            for i in xulie:
                i1 = i + 1
                tmp_url = down_url+'/' + str(i1).zfill(weishu) + '.mp3'
                url.append(urllib.request.quote(tmp_url, safe='/:?='))
        else:
            for item in _list:
                tmp_url = down_url + '/'+item + ".mp3"
                url.append(urllib.request.quote(tmp_url, safe='/:?='))
        return url

# 保存指定URL的文件
    def save_a_file(self, url, path, chapter):
        try:
            print('尝试下载',chapter)
            if not os.path.exists(path):
                response = requests.get(url)
                with open(path, 'wb') as f:
                    f.write(response.content)
                    f.close
                    print(chapter,'保存成功')
                response.close()
                time.sleep(1)
            else:
                print('文件已经存在')
        except:
            print('爬取失败,已下载至',chapter,'即将重新尝试下载')
            self.save_a_file(url, path, chapter)

    def download_files(self):
        result = self._getAllUrl()# 所有的章节对应的下载地址
        root = os.path.join(os.getcwd(), self.book_name)
        if not os.path.exists(root):
            os.mkdir(root)
        for index,i in enumerate(result):
            path = os.path.join(root, self.Chapter_list[index])+'.mp3'
            self.save_a_file(i, path, self.Chapter_list[index])
 print('aaa')
