from cli import screen
import re

import discord
from aiohttp.client_exceptions import ClientConnectionError
from discord import client
from rich.console import Console
from click import prompt, secho, confirm
from data import Screen, Notes, Settings, settings


discordClient = discord.Client()
screenObj = Screen()
notesObj = Notes()
settingsObj = Settings()

@discordClient.event
async def on_ready():
    secho('server ready!', fg='green')

@discordClient.event
async def on_message(message):
    if message.author == discordClient.user:
        return

    if '[dndsh' not in message.content:
        return

    # print(message.content)
    tags = re.findall(
        '\[(.*?)\]',
        message.content
    )

    async with message.channel.typing():
        for e in tags:
            t = e.split(':')
            
            if t[-1] not in screenObj.getListOfHexs():
                await message.channel.last_message.add_reaction('\N{THUMBS DOWN SIGN}')
                continue

            obj = screenObj.getByHex(t[-1])

            # TODO; add public notes
            await message.channel.send(
                file = discord.File(obj['picture'])
            )

            data = notesObj.readByScreenid(obj.doc_id, private=False)

            if data == []:
                continue

            msg = "**player notes** \n" #player notes
            for note in data:
                txt = "```\n"
                txt += note['text']
                txt += "\n```\n"
                msg += txt

            await message.channel.send(
                msg
            )

            data = notesObj.readByScreenid(obj.doc_id, private=True)
            
            Console().clear()
            Console().print('DM notes')
            for row in data:
                Console().print('>>>', row['text'])


if __name__ == '__main__':
    if settingsObj.exist('discord bot token') == False:
        token = prompt('Discord bot Token not found? pleses enter token')
        settingsObj.set('discord bot token', token)

    try:
        key = settingsObj.get('discord bot token')
        discordClient.run(key)
    except discord.errors.LoginFailure as err:
        secho('there has been an issue login', fg='red')
        if confirm('remove discord bot token?'):
            settingsObj.rmTag('discord bot token')
            secho('broken token has been removed', fg='yellow')
    
    except ClientConnectionError as err:
        secho("i can not conntect to discord are you connected to the internet?", fg='red')

    except Exception as err:
        secho('err: there has been a error | {}'.format(err), fg='red')
        print(type(err))
    
        