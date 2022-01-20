from tinydb import Query
from cli import segment

from data import SettingsData
from .base import BaseData
from .screen import _mkHex

class Segment(BaseData):

    def __init__(self, table: str = 'segment', requiredKeys='hex:str,title:str,text:str,campaign:int'):
        super().__init__(table, requiredKeys)

    def create(self, title:str, content:str, campaign:int) -> int:

        hex = ''
        while True:
            hex = _mkHex(4)

            while self.exists('hex', hex):
                continue
            break

        row = {
            'hex': hex,
            'title': title,
            'text': content,
            'campaign': campaign
        }
        return super().create(row)


    def readByCampaignId(self, campaign:id):

        db = self.createObj()
        rows = db.tbl.search(Query().campaign == campaign)
        db.close()

        return rows

    def readByHex(self, hex:str):

        db = self.createObj()
        row = db.tbl.get(Query().hex == hex)
        db.close()

        return row

    def readAllHex(self):
        rows = []
        activeCampign = SettingsData().get('Active Campain')

        for each in self.readAll():
            if each['campaign'] == activeCampign:
                rows.append(each['hex'])
        
        return rows

    def removeByHex(self, hex: hex):
        db = self.createObj()
        db.tbl.remove(Query().hex == hex)
        db.close()
        return True

    def addSegmentToString(self, text:str):

        temp = text

        for each in self.readAll():
            segmentTag = "{" + each['hex'] + "}"
            temp = temp.replace(segmentTag, temp)

        return temp
