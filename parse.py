import httpx
import threading
from lxml.etree import HTML
from getAPT import getAuthor, getPT

class Book:
    def __init__(self, page=1):
        self.ls = []
        self.page = page
    def _searchBook(self, title, page, publisher, author, isbn, year, doctype, lang_code, sort, orderby, onlylendable):
        searchUrl = "https://catalog.xmu.edu.cn/opac/openlink.php"
        params = {
            "title": title,
            "page": page,
            "publisher": publisher,
            "author": author,
            "isbn": isbn,
            "year": year,
            "doctype": doctype,
            "lang_code": lang_code,
            "sort": sort,
            "orderby": orderby,
            "onlylendable": onlylendable
        }
        searchResult = httpx.get(searchUrl, params=params)
        if searchResult.status_code != 200:
            return
        pageResult = HTML(searchResult.text)
        try:
            self.bookNum = int(pageResult.xpath("//*[@class='book_article']/div[1]/p/strong/text()")[0])
        except IndexError:
            self.bookNum = 0
        recordList = pageResult.xpath("//li[@class='book_list_info']")
        for record in recordList:
            bookDetail = {}
            bookDetail["link"] = searchUrl[:-12] + record.xpath("./h3/a/@href")[0]
            bookDetail["name"] = record.xpath("./h3/a//text()")[0].replace("/", "").strip()
            bookDetail["author"] = getAuthor(record.xpath("./p/text()")[1])
            bookDetail["press"], bookDetail["publishTime"] = getPT(record.xpath("./p/text()")[2], bookDetail["author"])
            bookDetail["copyNum"] = int(record.xpath("./p/span/text()")[0].strip()[-1])
            bookDetail["availableNum"] = int(record.xpath("./p/span/text()")[1].strip()[-1])
            self.ls.append(bookDetail)
    
    def startSearchBook(self, title, publisher, author, isbn, year, doctype, lang_code, sort, orderby, onlylendable):
        threads = []
        for i in range(self.page, self.page+20):
            t = threading.Thread(target=self._searchBook, kwargs={"title": title, "page": i, "publisher": publisher, "author": author, "isbn": isbn, "year": year, "doctype": doctype, "lang_code": lang_code, "sort": sort, "orderby": orderby, "onlylendable": onlylendable})
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        self.ls.sort(key=lambda some: int(some["name"].split(".")[0]))
        for i in range(len(self.ls)-1):
            if self.ls[i]["name"].split(".")[0] == self.ls[i+1]["name"].split(".")[0]:
                self.ls[i] = None
        self.ls = [book for book in self.ls if book is not None]
        return {"bookNum": self.bookNum, "recordInfo": self.ls}

    def getBookInfo(self, url):
        borrowInfo = []
        bookResult = httpx.get(url)
        if bookResult.status_code != 200:
            return borrowInfo
        bookPage = HTML(bookResult.text)
        try:
            copies = bookPage.xpath("//*[@class='whitetext']")
        except IndexError:
            return borrowInfo
        try:
            _ = copies[0].xpath("./td[1]/text()")[0].strip()
        except:
            return borrowInfo
        for copy in copies:
            borrowDetail = {}
            try:
                borrowDetail["index"] = copy.xpath("./td[1]/text()")[0].strip()
                borrowDetail["id"] = copy.xpath("./td[2]/text()")[0].strip()
                borrowDetail["volume"] = copy.xpath("./td[3]/text()")[0].strip()
                borrowDetail["location"] = copy.xpath("./td[4]/text()")[0].strip()
                borrowDetail["state"] = copy.xpath("./td[5]//text()")[0].strip()
            except:
                pass
            borrowInfo.append(borrowDetail)
        return borrowInfo
