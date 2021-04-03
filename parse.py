import httpx
from lxml.etree import HTML
from getAPT import getAuthor, getPT


def searchBook(title, page="1", publisher="", author="", isbn="", year="", doctype="ALL", lang_code="ALL", sort="M_AUTHOR", orderby="ASC", onlylendable="no"):
    searchUrl = "https://catalog.xmu.edu.cn/opac/openlink.php"
    bookUrl = "https://catalog.xmu.edu.cn/opac/"
    allRecord = {}
    allRecord["recordNum"] = 0
    allRecord["recordInfo"] = []
    for i in range(5):
        params = {
            "title": title,
            "page": str(i+int(page)),
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
            continue
        pageResult = HTML(searchResult.text)
        try:
            allRecord["recordNum"] = int(pageResult.xpath("//*[@class='book_article']/div[1]/p/strong/text()")[0])
        except IndexError:
            continue
        recordList = pageResult.xpath("//li[@class='book_list_info']")
        for record in recordList:
            bookDetail = {}
            bookDetail["link"] = bookUrl + record.xpath("./h3/a/@href")[0]
            bookDetail["name"] = record.xpath("./h3/a//text()")[0]
            bookDetail["author"] = getAuthor(record.xpath("./p/text()")[1])
            bookDetail["press"], bookDetail["publishTime"] = getPT(record.xpath("./p/text()")[2], bookDetail["author"])
            bookDetail["copyNum"] = int(record.xpath("./p/span/text()")[0].strip()[-1])
            bookDetail["availableNum"] = int(record.xpath("./p/span/text()")[1].strip()[-1])
            allRecord["recordInfo"].append(bookDetail)
    return allRecord


def getBookInfo(url):
    bookInfo = {}
    bookInfo["name"] = None
    bookInfo["author"] = None
    bookInfo["borrowInfo"] = []
    bookResult = httpx.get(url)
    if bookResult.status_code != 200:
        return bookInfo
    bookPage = HTML(bookResult.text)
    try:
        copies = bookPage.xpath("//*[@class='whitetext']")
    except IndexError:
        return bookInfo
    bookInfo["name"] = bookPage.xpath("//*[@id='item_detail']/dl[1]/dd/a/text()")[0]
    bookInfo["author"] = getAuthor(bookPage.xpath("//*[@id = 'item_detail']/dl[1]/dd/text()")[0])
    for copy in copies:
        borrowDetail = {}
        borrowDetail["index"] = copy.xpath("./td[1]/text()")[0].strip()
        borrowDetail["id"] = copy.xpath("./td[2]/text()")[0].strip()
        borrowDetail["volume"] = copy.xpath("./td[3]/text()")[0].strip()
        borrowDetail["location"] = copy.xpath("./td[4]/text()")[0].strip()
        borrowDetail["state"] = copy.xpath("./td[5]//text()")[0].strip()
        borrowDetail["ready"] = borrowDetail["state"] == "可借"
        bookInfo["borrowInfo"].append(borrowDetail)
    return bookInfo
