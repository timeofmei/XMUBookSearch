import httpx
from lxml.etree import HTML
from getAPT import getAuthor, getPT


def searchBook(title, page="1", publisher="", author="", isbn="", year="", doctype="ALL", lang_code="ALL", sort="M_AUTHOR", orderby="ASC", onlylendable="no"):
    searchUrl = "https://catalog.xmu.edu.cn/opac/openlink.php"
    allRecord = {}
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

        allRecord["recordNum"] = int(pageResult.xpath(
            "//*[@class='book_article']/div[1]/p/strong/text()")[0])
        recordList = pageResult.xpath("//li[@class='book_list_info']")

        for record in recordList:
            bookDetail = {}
            bookDetail["link"] = "https://catalog.xmu.edu.cn/opac/" + \
                record.xpath("./h3/a/@href")[0]
            print(bookDetail["link"])
            bookDetail["name"] = record.xpath("./h3/a//text()")[0]
            bookDetail["author"] = getAuthor(record.xpath("./p/text()")[1])
            bookDetail["press"], bookDetail["publishTime"] = getPT(
                record.xpath("./p/text()")[2], bookDetail["author"])
            bookDetail["copyNum"] = int(record.xpath(
                "./p/span/text()")[0].strip()[-1])
            bookDetail["availableNum"] = int(
                record.xpath("./p/span/text()")[1].strip()[-1])
            allRecord["recordInfo"].append(bookDetail)
    if allRecord == {}:
        return None
    return allRecord


def getBookInfo(bookUrl):
    bookResult = httpx.get(bookUrl)
    if bookResult.status_code != 200:
        return None
    bookPage = HTML(bookResult.text)
    copies = bookPage.xpath("//*[@class='whitetext']")
    bookInfo = {}
    bookInfo["borrowInfo"] = []
    i = 0
    bookInfo["name"] = bookPage.xpath(
        "//*[@id='item_detail']/dl[1]/dd/a/text()")[0]
    bookInfo["author"] = getAuthor(bookPage.xpath(
        "//*[@id = 'item_detail']/dl[1]/dd/text()")[0])
    for copy in copies:
        borrowDetail = {}
        borrowDetail["index"] = copy.xpath("./td[1]/text()")[0].strip()
        borrowDetail["id"] = copy.xpath("./td[2]/text()")[0].strip()
        borrowDetail["volume"] = copy.xpath("./td[3]/text()")[0].strip()
        borrowDetail["location"] = copy.xpath("./td[4]/text()")[0].strip()
        borrowDetail["state"] = copy.xpath("./td[5]//text()")[0].strip()
        borrowDetail["ready"] = int(copy.xpath(borrowDetail["state"] == "可借"))
        bookInfo["borrowInfo"].append(borrowDetail)
