from re import search
from discord import Client, File
from rich import print
from rich.console import Console
from rich.markdown import Markdown

from data import Screen, Notes


class LocalClient(Client):

    async def on_ready(self):
        print('Logged on:', self.user)

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if '[dm:' not in msg.content:
            return

        async with msg.channel.typing():

            tag = search('\[(.*?)\]', msg.content)
            ticket_val = tag.split(':')[-1]

            screenObj = Screen()

            if ticket_val not in screenObj.getListOfHexs():
                await msg.channel.last_message.add_reaction('\N{THUMBS DOWN SIGN}')
                return
            
            await msg.channel.last_message.add_reaction('\N{THUMBS UP SIGN}')
            doc = screenObj.getByHex(ticket_val)

            await msg.channel.send(
                file = File(doc['picture'])
            )

            notesObj = Notes()

            for note in notesObj.readByScreenid(screenid=doc.doc_id): #  gets public notes
                if note['noteType'] == 'text':
                    await msg.channel.send(
                        note['text']
                    )
                if note['noteType'] == 'file':
                    await msg.channel.send(
                        file=note['text']
                    )
            con = Console()
            con.clear()
            for note in notesObj.readByScreenid(screenid=doc.doc_id, private=True):
                if note['noteType'] == 'text':
                    con.print(Markdown(note['text']))
        pass

            