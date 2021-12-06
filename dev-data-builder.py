from posixpath import join
from random import choice
from faker import Faker

from os import rmdir, remove
from os.path import isdir, isfile
from glob import glob
from random import randint

from data import Campain, Screen
from rich import print
from rich.console import Console

con = Console()

def utill_rand_campId():
    ids = Campain().listDoc_ids()
    return int(choice(ids))

with con.status("starting build") as s:

    if isdir('.local'):
        for e in glob('.local/*'):
            remove(e)

        rmdir('.local')

    if isfile('ds.json'):
        remove('ds.json')

    cam = Campain()
    screen = Screen()
    f = Faker()
    s.update("createing campigns")

    for e in range(10):
        cam.create(
            f.name(),
            f.text()
        )

    s.update("createing screens")
    for e in range(100):
        screen.create(
            'https://www.youtube.com/watch?v=exskpUQQUtI',
            'https://joincake.imgix.net/neven-krcmarek-2Ni0lCRF9bw-unsplash.jpg?w=761&height=348&fit=crop&crop=edges&auto=format&dpr=1',
            title=f.name(),
            campain=utill_rand_campId(),
            pl_notes=f.text(),
            dm_notes=f.text()
        )
