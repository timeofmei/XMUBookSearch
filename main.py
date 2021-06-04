import ujson
from flask import Flask, request
from parse import Book
app = Flask(__name__)


@app.route('/', methods=["POST"])
def hello_world():
        reqData = ujson.loads(request.get_data().decode("utf-8"))
        bookUrl = reqData.get("bookUrl")
        if bookUrl is None:
            title = reqData.get("title")
            page = reqData.get("page") if reqData.get("page") else 1
            publisher = reqData.get("publisher") if reqData.get("publisher") else ""
            author = reqData.get("author") if reqData.get("author") else ""
            isbn = reqData.get("isbn") if reqData.get("isbn") else ""
            year = reqData.get("year") if reqData.get("year") else ""
            doctype = reqData.get("doctype") if reqData.get("doctype") else "ALL"
            lang_code = reqData.get("lang_code") if reqData.get("lang_code") else "ALL"
            sort = reqData.get("sort") if reqData.get("sort") else "M_AUTHOR"
            orderby = reqData.get("orderby") if reqData.get("orderby") else "ASC"
            onlylendable = reqData.get("onlyreadable") if reqData.get("onlyreadable") else "no"
            resData = ujson.dumps(Book(page=page).startSearchBook(title=title, publisher=publisher, author=author, isbn=isbn, year=year, doctype=doctype, lang_code=lang_code, sort=sort, orderby=orderby, onlylendable=onlylendable), ensure_ascii=False)
            return resData
        else:
            return ujson.dumps(Book().getBookInfo(bookUrl), ensure_ascii=False).encode("utf-8")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
