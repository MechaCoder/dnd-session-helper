from os.path import join
from ..base import BaseData, projectRoot

class History(BaseData):

    def __init__(self, file: str = 'ds.chat.history.json', table: str = 'history', requiredKeys: str='msg:str,sender:str,guildname:str,channel:str,ts:int'):
        super().__init__(table=table, requiredKeys=requiredKeys)
        self.fileName = join(projectRoot(), file)

    def create(self, msg:str, sender:str, server:str, channel:str) -> int:

        row = {
            'msg': msg,
            'sender': sender,
            'guildname': server,
            'channel': channel,
            'ts': round(self.now_ts())
        }
        return super().create(row)
