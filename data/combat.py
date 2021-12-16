from .base import BaseData
from tinydb import Query
from data import Screen


class EncounterData(BaseData): 
    
    def __init__(self, table: str = 'encounter', requiredKeys='name:str,url:str,screenHex:int'):
        super().__init__(table=table, requiredKeys=requiredKeys)

    def create(self, name:str, url:str, screenHex:int):

        if screenHex not in Screen().getListOfHexs():
            raise TypeError('hex has to be vaild')

        row = {
            'name': name,
            'url': url,
            'screenHex': screenHex
        }
        return super().create(row)

    def readByCompagn(self, campaign:int):
        db = self.createObj()
        rows = db.tbl.search(Query().campaign == campaign)
        db.close()

        return rows
