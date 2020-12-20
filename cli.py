from click import prompt, Path
from data import Screen

import click
from rich.table import Table
from rich import print, text

from pyperclip import copy

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
@click.option('--pic', '-p', type=click.Path(exists=True), prompt=True, help='this is a local img that apt repesents the screen')
@click.option('--soundtrack', '-s', type=str, prompt=True, help='this is the soundtrack to the sceen')
@click.option('--dm_notes', '-d', type=str, default='', help='the dm notes as a string')
@click.option('--pl_notes', '-p', type=str, default='', help='the player notes as a string')
def mk(title, pic, soundtrack, dm_notes, pl_notes):
    """ added a new screen. """
    newScreen = screenObj.create(soundtrack=soundtrack, picture=pic, title=title, dm_notes=dm_notes, pl_notes=pl_notes)
    click.secho('a new screen has been created, {}'.format(newScreen[1]), fg='green')

@screen.command()
def ls():
    





if __name__ == '__main__':
    cli()