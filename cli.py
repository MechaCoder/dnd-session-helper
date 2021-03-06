from click import prompt, Path
from data import Screen

import click
from rich.table import Table
from rich.console import Console
from rich import print, text

from pyperclip import copy

from interface.tables import listScreens
from interface.display import displayScreen

screenObj = Screen()
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
@click.option('--dm_notes', '-d', type=str, default='', help='the dm notes as a string')
@click.option('--pl_notes', '-p', type=str, default='', help='the player notes as a string')
def mk(title, pic, soundtrack, dm_notes, pl_notes):
    """ added a new screen. """
    newScreen = screenObj.create(soundtrack=soundtrack, picture=pic, title=title, dm_notes=dm_notes, pl_notes=pl_notes)
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
        dm_note = click.edit(doc['dm_notes'])
        screenObj.update_dm_notes(hex=hex, note=dm_note)
        click.secho('dm notes have been updated', fg='green')
        return 

    if ntype == 'pl':
        pl_note = click.edit(doc['pl_notes'])
        screenObj.update_pl_notes(hex=hex, note=pl_note)
        click.secho('pl notes have been updated', fg='green')
        return

@screen.command()
@click.argument('hex', type=click.Choice(listofhexValues))
def rm(hex):
    if click.confirm('are you sure you to delete {}?'.format(hex)) == False:
        return
    screenObj.removeByHex(hex)


if __name__ == '__main__':
    cli()