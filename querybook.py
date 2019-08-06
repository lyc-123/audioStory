from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import splider
class QuName:
    def __init__(self,number):
        self.number = number
    def getPageNum(self,url):
        f = requests.get(url)  # Get该网页从而获取该html内容
        soup = BeautifulSoup(f.content, "lxml")
        try:
            pageNum = soup.find('div', class_="pagesnums").find('span').text
            print('getPageNum执行成功')
            return int(pageNum[3:5])
        except:
            print('getPageNum执行失败')
        finally:
            print('___________________________')
    def getBookList(self):
        for num in range(1,self.number):
            pageNum = self.getPageNum('http://www.ting89.com/booklist/'+str(num)+'.html')
            self.getBookInfo('http://www.ting89.com/booklist/'+str(num)+'.html')
            print('http://www.ting89.com/booklist/'+str(num)+'.html')
            for num1 in range(2,pageNum):
                self.getBookInfo('http://www.ting89.com/booklist/'+str(num)+'_'+str(num1)+'.html')
                print('http://www.ting89.com/booklist/'+str(num)+'_'+str(num1)+'.html')

    def getBookInfo(self,url):
        f = requests.get(url)  # Get该网页从而获取该html内容
        soup = BeautifulSoup(f.content, "lxml")
        try:
            bookList = soup.find('div', class_="clist").findAll('li')
            for i in bookList:
                imgUrl = i.find('img')
                print('书籍封面',imgUrl['src'])
                # print('书名:',i.find('b').text)
                pList = i.findAll('p')
                for j in pList:
                    print(j.text)
                #下载文件
                splider.YsSpider(i.find('b').text).download_files()
        except:
            print('getBookInfo执行失败')
        finally:
            print('___________________________')

qn = QuName(13)         #这里是网站的类别数量(偷了个懒,直接写了个数字)
qn.getBookList()
