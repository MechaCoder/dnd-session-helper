import re
from os.path import isfile
from discord import Client, File
import discord
from rich import print
from rich.console import Console
from rich.markdown import Markdown

from data import Screen
from interface.display import displayScreen


class LocalClient(Client):

    async def on_ready(self):
        print('Logged on:', self.user)

    async def on_message(self, message):
        
        if message.author == self.user:
            return

        if '[dndsh' not in message.content:
            return

        async with message.channel.typing():

            tags = re.findall(
                '\[(.*?)\]',
                message.content
            )

            hex = tags[0].split(':')[-1]

            if hex not in Screen().getListOfHexs():
                await message.channel.last_message.add_reaction('\N{THUMBS DOWN SIGN}')
                return
            Console().clear()
            doc = displayScreen(hex)

            if isfile(doc['picture']):
                await message.channel.send(
                    file=doc['picture']
                )

            for paragraph in doc['pl_notes'].split('\n'):

                await message.channel.send(
                    paragraph
                )

        pass
