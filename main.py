import ujson
from flask import Flask, request
from parse import searchBook, getBookInfo
app = Flask(__name__)


@app.route('/', methods=["POST"])
def hello_world():
        reqData = ujson.loads(request.get_data().decode("utf-8"))
        print(type(reqData))
        bookUrl = reqData.get("bookUrl")
        if bookUrl is not None:
            return ujson.dumps(getBookInfo(bookUrl), ensure_ascii=False).encode("utf-8")
        else:
            title = reqData.get("title")
            page = reqData.get("page")
            publisher = reqData.get("publisher")
            author = reqData.get("author")
            isbn = reqData.get("isbn")
            year = reqData.get("year")
            doctype = reqData.get("doctype")
            lang_code = reqData.get("lang_code")
            sort = reqData.get("sort")
            orderby = reqData.get("orderby")
            onlylendable = reqData.get("onlyreadable")
            resData = ujson.dumps(searchBook(title=title, page=page, publisher=publisher, author=author, isbn=isbn, year=year, doctype=doctype, lang_code=lang_code, sort=sort, orderby=orderby, onlylendable=onlylendable), ensure_ascii=False)
            return resData


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
