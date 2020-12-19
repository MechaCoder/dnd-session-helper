from click import prompt, Path
from data import Notes, Screen

import click
from rich.table import Table
from rich import print, text

from pyperclip import copy

screenObj = Screen()
listofhexValues = screenObj.getListOfHexs()
notesObj = Notes()

@click.group()
def cli(): pass

@cli.group()
def screen(): pass

@screen.command()
@click.argument('title', type=str)
@click.option('--pic', type=click.Path(exists=True), prompt=True, help='this is a local img that apt repesents the screen')
@click.option('--soundtrack', type=str, prompt=True, help='this is the soundtrack to the sceen')
def mk(title, pic, soundtrack):
    """ added a new screen. """
    newScreen = screenObj.create(soundtrack=soundtrack, picture=pic, title=title)
    click.secho(
        'a new screen has been created, {}'.format(newScreen[1]),
        fg='green'
    )

@screen.command()
def ls():
    rows = screenObj.readAll()

    if rows == []:
        click.secho(
            'add some screens lazy !',
            fg='yellow'
        )
        return

    tbl = Table()
    tbl.add_column('hex')
    tbl.add_column('title')

    for row in screenObj.readAll():
        tbl.add_row(row['hex'], row['title'])

    print(tbl)

@screen.command()
@click.argument('hex', type=click.Choice(choices=listofhexValues, case_sensitive=True))
def rm(hex):
    screenObj.removeByHex(hex)
    click.secho(f'{hex} has been removed.', fg='green')

@screen.command()
@click.argument('hex', type=click.Choice(choices=listofhexValues, case_sensitive=True))
def cp(hex):
    "copys a hex information to the clipboard"
    # gets all the data
    sData = screenObj.getByHex(hex)

    msg = "-play {} \n [dndsh:{}]".format(sData['soundtrack'], hex)
    copy(msg)
    click.secho('tag copyed to clipboard', fg='green')
    return


@cli.group()
def notes(): pass

@notes.command()
@click.argument('screenHex', type=click.Choice(choices=listofhexValues, case_sensitive=True))
@click.option('--private', type=bool, default=True, prompt=True)
@click.option('--noteType', type=click.Choice(choices=['text', 'file']), default='text')
def mk(screenhex, private, notetype):
    doc = screenObj.getByHex(screenhex)

    if notetype == 'file':
        newNote = prompt('enter path to file', type=Path())
    if notetype == 'text':
        newNote = click.edit('')

    notesObj.create(doc.doc_id, text=newNote, private=private, noteType=notetype)
    click.secho('a need note has been added to screen: {}'.format(doc['hex']), fg='green')

@notes.command()
@click.option('--hexval', default='', type=click.Choice(choices=(listofhexValues + ['']), case_sensitive=True))
def ls(hexval):
    if hexval == '':
        data = notesObj.readAll()
    else:
        screenData = screenObj.getByHex(hexval)
        data = notesObj.readByScreenid(screenid=screenData.doc_id, private=False)
        data += notesObj.readByScreenid(screenid=screenData.doc_id, private=True)

    tbl = Table()
    tbl.add_column('text')
    tbl.add_column('private')

    for row in data:
        txt = row['text'][:50]
        txt = txt.replace('\n', '')
        tbl.add_row(txt, str(row['private']))

    print(tbl)

if __name__ == '__main__':
    cli()