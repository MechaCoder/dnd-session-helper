from os import get_terminal_size
from os.path import isfile
from random import choice
from PIL import Image

from data import Actions, Screen, Settings
from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from treelib import Tree
from treelib.exceptions import DuplicatedNodeIdError, NodeIDAbsentError

def showTree(rootHex:str):
    
    actions = Actions().readAll()
    screen = Screen()
    tree = Tree()

    tree.create_node(rootHex, rootHex)

    elementsTitle = {}
    for row in screen.readAll():
        try:
            elementsTitle[row['hex']] = row['title']
        except KeyError as err:
            pass

    i = 10
    while i > 0:
        for a in actions:
            try:
                if a == None:
                    continue
                t = "{} - {}".format(a['too'], elementsTitle[a['too']])
                tree.create_node(t, a['too'], parent=a['from'])
            except NodeIDAbsentError as err:
                # print(err)
                pass
            except DuplicatedNodeIdError as err:
                # print(err)
                pass
            except KeyError as err:
                pass

        i -= 1
    tree.show()


def displayScreen(hex, overRide=False):
    doc = Screen().getByHex(hex)

    if (Settings().get('displayServerSide') == False) or (overRide):
        return doc
    
    con = Console()

    tWidth, tHight = get_terminal_size()

    pl_string = doc['pl_notes']
    if pl_string == None:
        pl_string = ""

    pl_string = Markdown(pl_string)

    pl_notes_panel = Panel(
        title='Players Notes',
        renderable=pl_string,
        border_style="green"
    )

    dm_string = doc['dm_notes']
    if dm_string == None:
        dm_string = ""

    dm_string = Markdown(dm_string)

    dm_notes_panel = Panel(
        title='Dungeon Masters Notes ',
        renderable=dm_string,
        border_style="red"
    )

    tWidth = (tWidth / 2) - 1
    

    cols = Columns(
        renderables=[
            pl_notes_panel, 
            dm_notes_panel
        ],
        width=int(tWidth),
    )

    con.print(Text(
        doc['title'],
        justify='center'
    ))

    con.print(Rule(
        title=doc['hex'],
    ))

    e = ':thumbs_down:'
    if isfile(doc['picture']):
        e = ':thumbs_up:'


    try:
        img = Image.open(doc['picture'])
        img.show()
    except Exception:
        con.print(
            'picture - ', doc['picture'], e
        )

    con.print(
        'soundtrack - ', doc['soundtrack']
    )

    Console().print(cols)
    showTree(hex)

    return doc

    
