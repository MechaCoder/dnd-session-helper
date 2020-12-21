from typing import Set
from click import prompt
from click.utils import echo

from server import LocalClient
from data import Settings


if __name__ != '__main__':
    exit()
    
settings = Settings()
settingName = 'discord bot token'

if settings.exist(settingName) == False:
    token = prompt('Discord bot Token not found? pleses enter token', hide_input=True)
    settings.set(settingName, token)

try:
    key = settings.get(settingName)
    LocalClient().run(key)
except Exception as err:
    settings.rmTag(settingName)
