from os import get_terminal_size

from rich import align, columns
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.rule import Rule
from rich.console import Console

from pyfiglet import Figlet

from data import Screen

def displayScreen(hex):
    con = Console()
    doc = Screen().getByHex(hex)

    tWidth, tHight = get_terminal_size()
    
    pl_notes_panel = Panel(
        title='Players Notes',
        renderable=doc['pl_notes'],
        style="green"
    )
    dm_notes_panel = Panel(
        title='Dungeon Masters Notes ',
        renderable=doc['dm_notes'],
        style="red"
    )

    tWidth = (tWidth / 2) - 1

    cols = Columns(
        renderables=[pl_notes_panel, dm_notes_panel],
        width=int(tWidth),
    )

    title = Figlet(
        font='computer',
    )



    con.print(Text(
        title.renderText(doc['title']),
        justify='center'
    ))

    con.print(Rule(
        title=doc['hex'],
    ))

    con.print(
        Text('picture - '), doc['picture']
    )

    con.print(
        'soundtrack - ', doc['soundtrack']
    )

    Console().print(cols)

    return True

    
