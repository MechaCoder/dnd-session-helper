from data import Links
from rich.table import Table
from rich.text import Text
from rich.console import Console

def listOlinksAsTable():

    data = Links().readAll()

    tbl = Table('tag', 'url')

    for row in data:
        tagTxt = Text(row['tag'])
        valTxt = Text(row['val'])

        if len(tbl.rows) % 2 == 0:
            tagTxt.stylize("red")
            valTxt.stylize("red")

        tbl.add_row(tagTxt, valTxt)

    Console().print(tbl)
    return True

