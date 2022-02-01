from datetime import datetime
from os.path import abspath
from re import L

from click import clear
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Group, group
from rich.rule import Rule
from rich.markdown import Markdown

from data.history import History
from data import Screen, Players

from interface.display import displayScreen

def middleSection(hex:str):

    data = Screen().getByHex(hex)
    layout = Layout(name='middleSection')
    


    title = Text('TITLE:: {}'.format(data['title']))
    title.stylize("bold magenta", 0, 8)

    hexTxt = Text('HEX:: {}'.format(data['hex']))
    hexTxt.stylize("bold magenta", 0, 5)

    soundtrack = Text('SOUNDTRACK:: {}'.format(data['soundtrack']))
    soundtrack.stylize("bold magenta", 0, 12)

    picture = Text('background:: {}'.format( data['picture'] ) )
    picture.stylize("bold magenta", 0, 12)

    top = Layout(
        Group(
            title,
            hexTxt,
            soundtrack,
            picture
        ),
        ratio=1
    )

    bottom = Layout(ratio=7)
    bottom.split(
        # Panel(data['pl_notes'], title='players notes'), 
        Panel(
            Markdown(data['dm_notes']), 
                title="Dungeons master's Notes"
        )
    )


    layout.split(
        top,
        bottom
        
    )

    return Panel(layout, title='Screen')

class DmScreen():

    def pannelCurrentTime(self):

        sTimestamp = datetime.now().strftime('%H:%M:%S')

        return Panel(
            sTimestamp, 
            title='Current Time',
            # height=4
        )

    def pannelScreenTable(self):

        @group()
        def x():
            for row in Screen().readAll():

                x = " `" + row['hex'] + "` " + row['title']
                x = Text(x)
                x.stylize("bold red", 2, 6)
                x.stylize("italic", 8)
                x.overflow = 'crop'

                yield x
            

        return Panel(
            x(), 
            title='Screen Index',
            
        )

    def pannelLastMessage(self):

        obj = "" 
        rows = History().readAll()
        rows.reverse()
        
        for row in rows:

            obj += "[red]{}[/red] {} \n ".format(
                row['msg'][:10],
                row['ts']

            )

        return Panel(
            obj,
            title='Last Message',
        )

    def pannelDcTable(self):

        tbl = Table('Diffculty', 'DC', title="DC Table")
        tbl.add_row('Very Easy', '+5')
        tbl.add_row('Easy', '+10')
        tbl.add_row('Modrate', '+15')
        tbl.add_row('Hard', '+20')
        tbl.add_row('very hard', '+30')

        return Panel(tbl)

    def pannelPlayerTable(self):
        tbl = Table("name", "notes", title='Players')
        for row in Players().readAll():
            tbl.add_row(row['name'], row['notes'][:10])
        
        return Panel(tbl)

    def main(self, hex:str):
        clear()
        masterLayout = Layout(name='master')

        rightLayout = Layout(name='right')
        middleLayout = Layout(middleSection(hex), name='middle', ratio=3)
        leftLayout = Layout(name='left', ratio=1)

        leftLayout.split(
            Layout(self.pannelCurrentTime(), name='curTime'),
            Layout(self.pannelLastMessage(), name='lastMsg'),
            Layout(self.pannelScreenTable(), name='screenTbl', ratio=4),
        )

        rightLayout.split(
            self.pannelDcTable(),
            self.pannelPlayerTable()
        )

        masterLayout.split_row(
            rightLayout, middleLayout, leftLayout
        )

        Console().print(masterLayout)
        return True
