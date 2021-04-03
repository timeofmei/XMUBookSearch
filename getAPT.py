def getAuthor(string):
    if string.strip() == "":
        return "无"
    throwList = ["编注", "编著", "合著", "编著", "著", "撰稿", "主编", "撰稿人", "主办", "本卷", "主讲人", "主讲教师", "组织编译"]
    author = string
    author = author.replace(" ", "")
    author = author.replace("，", ",")
    for word in throwList:
        if word in author:
            author = author.replace(word, "")
    if "...[等]" in author:
        author = author.replace("...[等]", "等")
    author = author.strip("编写")
    author = author.strip("编")
    author = author.strip(",")
    return author


def getPT(string, author):
    press, year = string.split("\xa0")
    press = press.strip()
    if press == "编者":
        press = author
    year = year.replace(" ", "")
    year.strip("-")
    try:
        _ = float(year)
    except:
        year = year.replace(".", "")
        year = year.replace("[", "")
        year = year.replace("]", "")
        if "年" in year:
            for i in range(10):
                year = year.replace(str(i), "")
    return press, year
