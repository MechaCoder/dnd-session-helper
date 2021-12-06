from ..base import BaseData

class History(BaseData):

    def __init__(self, file: str = 'ds.chat.history.json', table: str = 'history', requiredKeys: str='msg,sender,guildname,channel,ts'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, msg:str, sender:str, server:str, channel:str) -> int:

        row = {
            'msg': msg,
            'sender': sender,
            'guildname': server,
            'channel': channel,
            'ts': round(self.now_ts())
        }
        return super().create(row)
