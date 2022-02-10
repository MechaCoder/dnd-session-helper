from rich.table import Table
from data import Screen

def listScreens(all:bool):

    tbl = Table()
    tbl.add_column('hex')
    tbl.add_column('title')
    
    for row in Screen().readAll(all=all):
        tbl.add_row(row['hex'], row['title'])

    return tbl

