import json
from flask import Flask, request
from parse import searchBook, getBookInfo
app = Flask(__name__)


@app.route('/', methods=["POST"])
def hello_world():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    try:
        bookUrl = json_data.get("bookUrl")
        return getBookInfo(bookUrl)
    except:
        title = json_data.get("title")
        page = json_data.get("page")
        publisher = json_data.get("publisher")
        author = json_data.get("author")
        isbn = json_data.get("isbn")
        year = json_data.get("year")
        doctype = json_data.get("doctype")
        lang_code = json_data.get("lang_code")
        sort = json_data.get("sort")
        orderby = json_data.get("orderby")
        onlylendable = json_data.get("onlyreadable")
        return searchBook(title=title, page=page, publisher=publisher, author=author, isbn=isbn, year=year, doctype=doctype, lang_code=lang_code, sort=sort, orderby=orderby, onlylendable=onlylendable)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
