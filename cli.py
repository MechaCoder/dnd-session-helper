from datetime import datetime
from os import remove
from time import sleep

import click
from click.termui import edit, secho
from faker.proxy import Faker
from pyperclip import copy
from rich import print
from rich.console import Console
from rich.table import Table

from data import Actions
from data import CampainData as Campain
from data import CombatData, History, Screen, Settings, campain
from data.api import MonstersIndex
from data.combat import NpcData
from interface.combat import CombatDisplay
from interface.display import displayScreen
from interface.export import export as exporter
from interface.generate import displayComplexNPC, displaySimpleNPC
from interface.tables import listScreens

screenObj = Screen()
campainObj = Campain()
listofhexValues = screenObj.getListOfHexs()

@click.group()
def cli(): pass

@cli.group()
def screen():
    """ Screens are a colection of player notes, dm notes, soundtrack and a picture """
    pass

@screen.command()
def template():
    "edit the dm notes template used."

    setttingsObj = Settings()
    oldtemplate = setttingsObj.get('screenTemplate')
    newtemplate = edit(oldtemplate)

    if newtemplate == None:
        newtemplate = ''
    
    setttingsObj.set('screenTemplate', newtemplate)


    secho('template changed')


@screen.command()
@click.argument('title', type=str)
@click.option('--pic', '-p', type=str, prompt=True, help='this is a local img that apt repesents the screen')
@click.option('--soundtrack', '-s', type=str, prompt=True, help='this is the soundtrack to the sceen')
@click.option('--dm_notes', type=str, default='', help='the dm notes as a string')
@click.option('--pl_notes', type=str, default='', help='the player notes as a string')
# @click.option('--campain',  type=click.Choice(campainidList), default=0)
def mk(title, pic, soundtrack, dm_notes, pl_notes):
    """ added a new screen. """
    if dm_notes == '':
        dm_notes = Settings().get('screenTemplate')

    newScreen = screenObj.create(
        soundtrack=soundtrack, 
        picture=pic, 
        title=title, 
        dm_notes=dm_notes, 
        pl_notes=pl_notes
    )
    click.secho('a new screen have been created, {}'.format(newScreen[1]), fg='green')

@screen.command()
def ls():
    """prints out a table of all screens in the system"""
    lis = listScreens()
    Console().print(lis)

@screen.command()
@click.argument('hex', type=click.Choice(listofhexValues))
def cat(hex):
    """ displays a screen """
    displayScreen(hex, overRide=False)

@screen.command()
@click.argument('hex', type=click.Choice(listofhexValues))
def cp(hex):
    """ copys a screen data elemem to  the clipboard. """
    doc = screenObj.getByHex(hex)
    msg = "-play {} \n [dndsh:{}]".format(
        doc['soundtrack'],
        hex
    )
    copy(msg)


@screen.group()
def update():
    """ update screen values """
    pass

@update.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('title', type=str)
def title(hex, title):
    """updates the title"""
    screenObj.update_title(hex=hex, title=title)
    click.secho('title have been updated', fg='green')

@update.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('soundtrack', type=str)
def soundtrack(hex, soundtrack): 
    """updates the soundtrack"""
    screenObj.update_soundtrack(hex=hex, soundtrack=soundtrack)
    click.secho('soundtrack have been updated', fg='green')

@update.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('picture', type=click.Path(exists=True, file_okay=True))
def picture(hex, picture):
    """ updates the picture for a screen"""
    # TODO: dose the old picture get deleted
    screenObj.update_picture(hex=hex, picture=picture)
    click.secho('picture have been updated', fg='green')
    pass

@update.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('ntype', type=click.Choice(['dm', 'pl']), default='dm')
def notes(hex, ntype):
    """update the screens nots"""
    
    doc = screenObj.getByHex(hex)

    if ntype == 'dm':
        dm_note = click.edit(text=doc['dm_notes'])
        if isinstance(dm_note, str):
            screenObj.update_dm_notes(hex=hex, note=dm_note)
            click.secho('dm notes have been updated', fg='green')
        return 

    if ntype == 'pl':
        pl_note = click.edit(text=doc['pl_notes'])
        if isinstance(pl_note, str):
            screenObj.update_pl_notes(hex=hex, note=pl_note)
            click.secho('pl notes have been updated', fg='green')
        return

@screen.command()
@click.argument('hex', type=click.Choice(listofhexValues))
def rm(hex):
    """removes a screen by hex"""

    if click.confirm('are you sure you to delete {}?'.format(hex)) == False:
        return
    row = screenObj.getByHex(hex)
    remove(row['picture'])
    screenObj.removeByHex(hex)
    Actions().removeByHex(hex)

@screen.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('title', type=str)
def cp(hex, title):
    row = screenObj.copyScreen(
        hex,
        title
    )
    secho('copy of {} has been made and the hex is {}'.format(hex, row[1]), fg='green')

@screen.group()
def combat(): pass

combat_ids = CombatData().readDoc_ids()

@combat.command()
@click.argument('combat_id', type=click.Choice(combat_ids) )
def run(combat_id):
    """runs a combat based on the combat id."""
    combat_id = int(combat_id)
    CombatDisplay(combat_id).run()
    pass


@combat.command()
@click.argument('title', type=str)
@click.argument('hex', type=click.Choice(listofhexValues))
@click.option('--notes', type=str, default=1)
def mk(title, hex, notes):
    """creates a combat"""
    CombatData().create(
        screenHex=hex,
        title=title,
        notes=notes
    )
    click.secho('a combat ({}) has been created for {}'.format(title, hex))
    pass

@combat.command()
@click.argument('doc_id', type=click.Choice(CombatData().readDoc_ids()))
def rm(doc_id):
    """removes a combat"""
    doc_id = int(doc_id)
    CombatData().removeById(doc_id=doc_id,)
    click.secho('a combat has been removed.', fg='green')
    pass


@combat.command()
@click.argument('screenHex', type=click.Choice(listofhexValues))
def ls(screenhex):
    """lists the comabats attached to a screen"""
    
    tbl = Table()
    tbl.add_column('id')
    tbl.add_column('title')
    tbl.add_column('notes')
    tbl.add_column('npcs')

    npcs = NpcData()

    for each in CombatData().readByHex(screenhex):
        n = npcs.readByHex(each.doc_id)
        
        text = ""
        for e in n:
            text += '[red]{}({}) - {}[/red], '.format(e['name'], e.doc_id, e['index'])
        tbl.add_row( str(each.doc_id), each['title'], each['notes'], text)

    Console().print(tbl)

@combat.group()
def npc(): pass

indexChoices = MonstersIndex().readAllIndex()
randomName = Faker().first_name()
combat_ids = CombatData().readDoc_ids()

@npc.command()
@click.argument('index', type=click.Choice(indexChoices))
@click.argument('combat_id', type=click.Choice(combat_ids))
@click.option('--name', type=str, default=randomName)
def mk(name, index, combat_id):
    """ creates a npc"""

    NpcData().create(
        name=name,
        index=index,
        combat_id=combat_id
    )

doc_ids = NpcData().readDoc_ids()

@npc.command()
@click.argument('doc_ids', type=click.Choice(doc_ids))
def rm(doc_ids):
    """ removes npc """
    NpcData().removeById(doc_ids)

@cli.group()
def campaign(): pass

@campaign.command()
@click.argument('title', type=str)
@click.option('--bio', type=str, default='')
def mk(title, bio):
    """ creates a new campaign"""
    Campain().create(
        title=title,
        bio=bio
    )

@campaign.command()
def ls():
    """lists all campagns"""
    tbl = Table()
    tbl.add_column('id')
    tbl.add_column('title')
    tbl.add_column('bio')
    tbl.add_column('active')

    activeId = Settings().get('Active Campain')
    
    for row in Campain().readAll():
        a = ''

        if row.doc_id == activeId:
            a = ":white_check_mark:"

        tbl.add_row(str(row.doc_id), row['title'], row['bio'], a)

    Console().print(tbl)

campainidList = campainObj.readDoc_ids()

@campaign.command()
@click.argument('campain_id', type=click.Choice(campainidList))
def active(campain_id):
    """ changes the active campaign id"""
    campain_id = int(campain_id)
    a = Settings().set('Active Campain', campain_id)
    click.secho('campain {} has be set as active'.format(campain_id), fg='green')

@cli.group()
def chat():
    """ this is a interaction on the discord server. """
    pass

@chat.command()
def read():
    """ this is allows dm to read the recourd"""
    hist = History()

    tbl = Table()
    tbl.add_column('doc_id')
    tbl.add_column('sender')
    tbl.add_column('guildname')
    tbl.add_column('channel')
    tbl.add_column('ts')
    tbl.add_column('message')

    for row in hist.readAll():
        ts = row['ts']
        ts = datetime.fromtimestamp(ts).strftime('%H:%M %d/%m/%y')

        tbl.add_row(
            str(row.doc_id),
            row['sender'],
            row['guildname'],
            row['channel'],
            str(ts),
            row['msg']
        )
    Console().print(tbl)

@chat.command()
def clear():
    History().clear()
    click.secho('chat history has been cleared')

@cli.group()
def settings(): pass


@settings.command()
def get():
    """ shows a table of all setings that exist """
    tbl = Table()
    tbl.add_column('tag')
    tbl.add_column('value')
    
    for row in Settings().getAll():
        tbl.add_row(
            row['tag'], 
            str(row['val']).strip()
        )
    Console().print(tbl)

@settings.command()
@click.argument('tag', type=click.Choice(Settings().readTags()))
@click.argument('val', type=any)
def set(tag, val):
    """set a setting from excistings"""
    Settings().set(tag, val)

@cli.group()
def gen(): 
    """ there is a genrateor for NPCs """
    pass

@gen.command()
def complex():
    """ gen a complex profile on NPC"""
    char = displayComplexNPC()
    Console().print(char)

@gen.command()
def simple():
    """ gen a simple NPC"""
    char = displaySimpleNPC()
    Console().print(char)

@cli.command()
@click.option('--hours', type=int, default=0)
@click.option('--minute', type=int, default=0)
@click.argument('secounds', type=int, default=0)
def countdown(hours:int, minute:int, secounds:int):
    """creates a countdown timer for breaks and timeed activites"""
    timerSecs = secounds
    timerSecs += (minute * 60)
    timerSecs += (hours * 3600)

    with Console().status('countdown', spinner='clock') as status:
        while timerSecs:
            sleep(1)    
            status.update(f'counting down [{timerSecs}]')
            timerSecs -= 1
    pass

@cli.command()
@click.argument('campain_id', type=click.Choice(campainidList))
def export(campain_id):
    """exports a campagin to pdf and doc"""
    campain_id = int(campain_id)
    exporter(campain_id)

@cli.group()
def actions():
    """this enables the dm to create connections """ 
    pass

@actions.command()
@click.argument('from_hex', type=click.Choice(listofhexValues))
@click.argument('to_hex', type=click.Choice(listofhexValues))
def mk(from_hex, to_hex):
    """actions create links between between screens"""
    Actions().create(
        from_tag=from_hex,
        to_tag=to_hex
    )
    Console().print("new action created")

@actions.command()
@click.argument('from_hex', type=click.Choice(listofhexValues))
@click.argument('to_hex', type=click.Choice(listofhexValues))
def rm(from_hex, to_hex):
    Actions().removeAllByHex(from_hex=from_hex, to_hex=to_hex)
    secho('actions have been deleted')

if __name__ == '__main__':
    cli()
