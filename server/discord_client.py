import re
from os.path import isfile
from discord import Client, File
import discord
from rich import print
from rich.console import Console
from rich.markdown import Markdown

from data import Screen
from interface.display import displayScreen
from data.dice import roller


class LocalClient(Client):

    async def on_ready(self):
        print('Logged on:', self.user)

    async def on_message(self, message):
        
        if message.author == self.user:
            return

        if '[dndsh' in message.content:
            await self._message_content_tags(message)
            return

        if '(roll:' in message.content:
            await self._dice_roller(message)
            return

    async def _message_content_tags(self, message):
        
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
                    file=discord.File(doc['picture']) 
                )

            for paragraph in doc['pl_notes'].split('\n'):

                if paragraph == '':
                    continue

                await message.channel.send(
                    paragraph
                )
            
            return True

    async def _dice_roller(self, message):

        tags = re.findall(
            '\((.*?)\)',
            message.content
        )

        for tag in tags:
            tag = tag.split(':')[-1]
            obj = roller(tag)

            msg = "```\n roll total: {} \n roll list:  {} ```".format(
                obj['sum'],
                obj['rolls']
            )

            await message.channel.send(
                msg
            )

        return 

