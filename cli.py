from random import choice
from datetime import date, datetime
from os import remove

from rich import console

from data.campain import CampainData
from click import prompt, Path
from data import Screen, Campain, Settings, Combat, History

import click
from rich.table import Table
from rich.console import Console
from rich import print, text
from pyperclip import copy

from interface.tables import listScreens
from interface.display import displayScreen
from interface.generate import displayComplexNPC


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
@click.argument('title', type=str)
@click.option('--pic', '-p', type=str, prompt=True, help='this is a local img that apt repesents the screen')
@click.option('--soundtrack', '-s', type=str, prompt=True, help='this is the soundtrack to the sceen')
@click.option('--dm_notes', type=str, default='', help='the dm notes as a string')
@click.option('--pl_notes', type=str, default='', help='the player notes as a string')
# @click.option('--campain',  type=click.Choice(campainidList), default=0)
def mk(title, pic, soundtrack, dm_notes, pl_notes):
    """ added a new screen. """
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
    displayScreen(hex)

@screen.command()
@click.argument('hex', type=click.Choice(listofhexValues))
def cp(hex):
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
    screenObj.update_title(hex=hex, title=title)
    click.secho('title have been updated', fg='green')

@update.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('soundtrack', type=str)
def soundtrack(hex, soundtrack): 
    screenObj.update_soundtrack(hex=hex, soundtrack=soundtrack)
    click.secho('soundtrack have been updated', fg='green')

@update.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('picture', type=click.Path(exists=True, file_okay=True))
def picture(hex, picture): 
    screenObj.update_picture(hex=hex, picture=picture)
    click.secho('picture have been updated', fg='green')
    pass

@update.command()
@click.argument('hex', type=click.Choice(listofhexValues))
@click.argument('ntype', type=click.Choice(['dm', 'pl']), default='dm')
def notes(hex, ntype):
    
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
    if click.confirm('are you sure you to delete {}?'.format(hex)) == False:
        return
    row = screenObj.getByHex(hex)
    remove(row['picture'])
    screenObj.removeByHex(hex)

@cli.group()
def campaign(): pass

@campaign.command()
@click.argument('title', type=str)
@click.option('--bio', type=str, default='')
def mk(title, bio):
    Campain().create(
        title=title,
        bio=bio
    )

@campaign.command()
def ls():
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

campainidList = campainObj.listDoc_ids()
campainidList.append('0')

@campaign.command()
@click.argument('campain_id', type=click.Choice(campainidList))
def active(campain_id):
    Settings().set('Active Campain', campain_id)
    click.secho('campain {} has be set as active'.format(campain_id), fg='green')

@cli.group()
def combat(): pass

@combat.command()
@click.argument('name', type=str)
@click.argument('url', type=str)
def mk(name, url):
    Combat().create(name=name, url=url)
    click.secho('a new encounter has been created', fg='green')

@combat.command()
def ls():
    tbl = Table()
    tbl.add_column('doc id')
    tbl.add_column('name')
    tbl.add_column('url')
    
    for row in Combat().readAll():
        tbl.add_row(str(row.doc_id) , row['name'], row['addr'])
    Console().print(tbl)

@combat.command()
@click.argument('combat_id', type=click.Choice(Combat().readDoc_ids()))
def rm(combat_id):
    Combat().removeById(combat_id)
    click.secho('combat deleted.', fg='red')

@cli.group()
def chat():
    """ this is a interaction """
    pass

@chat.command()
def read():
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
    Settings().set(tag, val)

@cli.group()
def gen(): 
    """ there is a genrateor for NPCs """
    pass

@gen.command()
def complex():
    char = displayComplexNPC()
    Console().print(char)
    

if __name__ == '__main__':
    cli()
