from os import get_terminal_size
from os.path import isfile

from rich import align, columns
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.rule import Rule
from rich.console import Console
from rich.markdown import Markdown

from pyfiglet import Figlet

from data import Screen

def displayScreen(hex):
    con = Console()
    doc = Screen().getByHex(hex)

    tWidth, tHight = get_terminal_size()

    pl_string = doc['pl_notes']
    if pl_string == None:
        pl_string = ""

    pl_string = Markdown(pl_string)

    pl_notes_panel = Panel(
        title='Players Notes',
        renderable=pl_string,
        style="green"
    )

    dm_string = doc['dm_notes']
    if dm_string == None:
        dm_string = ""

    dm_string = Markdown(dm_string)

    dm_notes_panel = Panel(
        title='Dungeon Masters Notes ',
        renderable=dm_string,
        style="red"
    )

    tWidth = (tWidth / 2) - 1
    

    cols = Columns(
        renderables=[
            pl_notes_panel, 
            dm_notes_panel
        ],
        width=int(tWidth),
    )

    title = Figlet(
        font='computer',
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

    con.print(
        'picture - ', doc['picture'], e
    )

    con.print(
        'soundtrack - ', doc['soundtrack']
    )

    Console().print(cols)

    return doc

    
