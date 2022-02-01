import re
from os.path import isfile
from click.decorators import group
from discord import Client, File
import discord
from discord.channel import DMChannel, TextChannel
from discord.gateway import DiscordClientWebSocketResponse
from rich import print
from rich import table
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from playsound import playsound
from threading import Thread
from os import popen

from data import Screen, History, Settings, settings, Players
from interface.display import displayScreen
<<<<<<< Updated upstream
from data.dice import roller, DiceHistory
=======
from interface.dm_screen import DmScreen
>>>>>>> Stashed changes
from server.notfications import pushNoteCards

history = History()
settingsObj = Settings()
dms_screen = DmScreen()

class LocalClient(Client):

    async def on_ready(self):
        DiceHistory().clear()
        print('Logged on:', self.user)

    async def on_message(self, message):

        if settingsObj.get('chatHistory'):
            history.create(
                msg=message.content,
                sender=message.author.name,
                server=message.guild.name,
                channel=message.channel.name
            )
        
        if message.author == self.user:
            return

        if isinstance(message.channel, DMChannel):
            #if a user dm's the bot
            await self._dm_controller(message)
            pass

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
<<<<<<< Updated upstream
            doc = displayScreen(hex)
=======
            doc = Screen().getByHex(hex)
            if Settings().get('displayServerSide'):
                dms_screen.main(hex)
>>>>>>> Stashed changes

            if isfile(doc['picture']) or doc['picture'] == '':
                await message.channel.send(
                    file=discord.File(doc['picture']) 
                )

            await message.channel.send(
                doc['soundtrack']
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

    async def _dm_controller(self, message):

        player = Players()
        activeCampaign = Settings().get('Active Campain')


        if 'xcard' in message.content.lower():

            pushNoteCards(
                message.author.name,
                'x-Card'
            )

        if 'rewind' in message.content.lower():
            pushNoteCards(
                message.author.name,
                'rewind'
            )

        if 'fast-forward' in message.content.lower():
            pushNoteCards(
                message.author.name,
                'fast forward'
            )

        if 'pause' in message.content.lower():
            pushNoteCards(
                message.author.name,
                'pause'
            )

        

        
        if player.playerExistsInCampaign(message.author.name, activeCampaign) is False:
            await message.channel.send(
                f'hey {message.author.name}, let me save your information.'
            )

            pid = player.create(
                message.author.name,
                activeCampaign
            )

            await message.channel.send(
                'saved...'
            )

        
        pass

