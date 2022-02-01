from os import get_terminal_size
from os.path import isfile
from random import choice
from PIL import Image

from data import Actions, Screen, Settings, CampainData, Segment
from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.tree import Tree
from treelib.exceptions import DuplicatedNodeIdError, NodeIDAbsentError

def tree(hex):
    screenObj = Screen()

    first_screen = screenObj.readByHex(hex)['title']
    tree = Tree(f'{hex} {first_screen}')

    branch_hexs = []

    for e in Actions().readActions(hex):
        x = e['too']
        scr = screenObj.readByHex(e['too'])['title']

        if x not in branch_hexs:
            tree.add(f'{x} {scr}')
            branch_hexs.append(x)
    

    return tree

def displayScreen(hex:str):
    
    doc = Screen().getByHex(hex)
    cam = CampainData().readById(doc_id=doc['campain'])
    temSize = get_terminal_size()

    masterLayout = Layout(name='master')

    firstPannel = Layout(name='object')

    topLeft = Table.grid(expand=True)
    topLeft.add_column()
    topLeft.add_column()
    topLeft.add_row('[green]soundtrack', doc['soundtrack'])
    topLeft.add_row('[green]background', doc['picture'])
    topLeft.add_row('[green]campaign', cam['title'])
    topLeft.add_row('[green]campaign bio', cam['bio'])


    firstPannel.split_row(
        topLeft, Panel(tree(hex), title='actions')
    )

    notes = Layout(name='notes', ratio=5)
    notes.split_row(
        Panel(doc['pl_notes'], title="Player's Notes", border_style="green"),
        Panel(Markdown(doc['dm_notes']), title="Master's Notes", border_style="red")
    )

    masterLayout.split(
        firstPannel, 
        notes
    )

    img = Image.open(doc['picture'])
    img.show()

    return Panel(masterLayout, height=(temSize.lines - 2), title=doc['title'])
    

def tableOfSegment():

    campaign = Settings().get('Active Campain')
    segs = Segment().readByCampaignId(campaign)

    tbl = Table(
        'hex', 'title'
    )

    for each in segs:

        tbl.add_row(
            each['hex'],
            each['title']
        )

    return tbl


