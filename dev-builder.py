from posixpath import join
from random import choice
from faker import Faker
from mdgen import MarkdownPostProvider

from os import mkdir, rmdir, remove
from os.path import isdir, isfile
from glob import glob
from random import randint

from data import CampainData as Campain, Screen, Actions, Players
from rich import print
from rich.console import Console

from data.combat import CombatData, NpcData, MonstersIndex

con = Console()

def randomised_screen_hex():
    pool = []

    for x in range(1000):
        pool.append(
            choice(
                Screen().getListOfHexs()
            )
        )


    return choice(pool)


def utill_rand_campId():
    ids = Campain().listDoc_ids()
    return int(choice(ids))

with con.status("starting build") as s:

    if isfile('.dev') == False:
        con.print('createing .dev file')
        open('.dev', 'a').close()

    if isdir('.local_dev'):
        con.print('createing .local_dev/ dircector')
        for e in glob('.local_dev/*'):
            remove(e)

        rmdir('.local_dev')
    mkdir('.local_dev')

    if isfile('ds.dev.json'):
        remove('ds.dev.json')

    cam = Campain()
    screen = Screen()
    actions = Actions()
    f = Faker()
    f.add_provider(MarkdownPostProvider)

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
            pl_notes=f.post(size='large'),
            dm_notes=f.post(size='large')
        )

    s.update("creating actions")
    # for from_hex in Screen().getListOfHexs():
    hexPool = Screen().getListOfHexs()
    for e in range(100):
        try:
            Actions().create(choice(hexPool), choice(hexPool))
        except Exception as err:
            pass

    s.update('createing players')
    for e in range(50):
        randCampaign = choice(cam.readAll())
        Players().create(
            Faker().name(),
            randCampaign.doc_id,
        )

    s.update('createing combat')
    for e in range(50):
        obj = choice(Screen().readAll())
        CombatData().create(
            obj['hex'],
            Faker().name(),
            Faker().text()
        )

    s.update('create npcs')
    for e in range(50):
        rand = choice(CombatData().readAll())
        randMonster = choice(MonstersIndex().readAll())
        NpcData().create(
            Faker().name(),
            randMonster['index'],
            rand.doc_id
        )