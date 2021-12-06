from random import choice
from faker import Faker
from data import Campain, Screen
from rich import print
from rich.console import Console

con = Console()

def utill_rand_campId():
    ids = Campain().listDoc_ids()
    return int(choice(ids))

with con.status("starting build") as s:

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
    x = f.name()
    print(x)

    for e in range(10):
        screen.create(
            'https://www.youtube.com/watch?v=exskpUQQUtI',
            'https://joincake.imgix.net/neven-krcmarek-2Ni0lCRF9bw-unsplash.jpg?w=761&height=348&fit=crop&crop=edges&auto=format&dpr=1',
        )
