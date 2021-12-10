from .base import BaseData
from tinydb import Query

class EncounterData(BaseData): 
    
    def __init__(self, table: str = 'encounter', requiredKeys='name:str,url:str,campaign:int'):
        super().__init__(table=table, requiredKeys=requiredKeys)

    def create(self, name:str, url:str, campaign_id:int):
        row = {
            'name': name,
            'url': url,
            'campaign': campaign_id
        }
        return super().create(row)

    def readByCompagn(self, campaign:int):
        db = self.createObj()
        rows = db.tbl.search(Query().campaign == campaign)
        db.close()

        return rows
