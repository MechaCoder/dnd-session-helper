import re
from os.path import isfile
from click.decorators import group
from discord import Client, File
import discord
from discord.gateway import DiscordClientWebSocketResponse
from rich import print
from rich import table
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from data import Screen, History, Settings, settings
from interface.display import displayScreen
from data.dice import roller, DiceHistory

history = History()
settingsObj = Settings()

class LocalClient(Client):

    async def on_ready(self):
        DiceHistory().clear()
        print('Logged on:', self.user)

    async def on_message(self, message):

        if settingsObj.get('chat History'):
            history.create(
                msg=message.content,
                sender=message.author.name,
                server=message.guild.name,
                channel=message.channel.name
            )
        
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

            if hex.lower() == 'ping':
                await message.channel.send('I am ready to play')
                return True

            if hex not in Screen().getListOfHexs():
                await message.channel.last_message.add_reaction('\N{THUMBS DOWN SIGN}')
                return

            
            Console().clear()
            doc = displayScreen(hex)

            if isfile(doc['picture']) or doc['picture'] == '':
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

        async with message.channel.typing():

            for tag in tags:
                tag = tag.split(':')[-1]

                if tag == 'history':
                    
                    msg = "dice roll history \n ```"
                    for row in DiceHistory().readAll():
                        # print(row)
                        msg += 'at {}, a user requested {} and got {} \n'.format(
                            str(row['ts']),
                            row['slug'],
                            row['result']
                        )
                    msg += '\n```'
                    
                    await message.channel.send(
                        msg
                    )
                    return

                else:

                    obj = roller(tag)

                    msg = "```\n roll total: {} \n roll list:  {} ```".format(
                        obj['sum'],
                        obj['rolls']
                    )

                    await message.channel.send(
                        msg
                    )

        return 

