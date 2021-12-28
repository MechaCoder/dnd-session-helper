from tinydb.queries import Query
from .base import BaseData

class Players(BaseData):

    def __init__(self, table: str = 'Player', requiredKeys='name:str,notes:str,campagin:int'):
        super().__init__(table=table, requiredKeys=requiredKeys)

    def create(self, name:str, campaingn:int, notes:str = ''):
        row = {
            'name': name,
            'campagin': campaingn,
            'notes': notes
        }
        return super().create(row)

    def readByCampaignId(self, id:int):

        db = self.createObj()
        data = db.tbl.search(Query()['campagin'] == id)
        db.close()

        return data

    def playerExistsInCampaign(self, name:str, campagin:int):

        db = self.createObj()
        qry = Query()
        data = db.tbl.contains(
            (qry.name == name) & (qry.campagin == campagin)
        )
        db.close()

        return data