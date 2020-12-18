from cli import screen
import re

import discord
from discord import client
from rich.console import Console

from data import Screen, Notes

discordClient = discord.Client()
screenObj = Screen()
notesObj = Notes()

@discordClient.event
async def on_ready():
    print('server ready!')

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
            
            

discordClient.run('Nzg5MTgxNTMzMzg2NDQwNzc1.X9uUkw.JO5Rpplw9S1NymGXylUa-Qf7sNs')