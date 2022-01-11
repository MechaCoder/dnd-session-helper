from tinydb import Query
from .base import BaseData
from .screen import ScreenData

class Actions(BaseData):

    def __init__(self, table: str = "actionData", requiredKeys='from:str,too:str'):
        super().__init__(table=table, requiredKeys=requiredKeys)

    def create(self, from_tag:str, to_tag:str):

        obj = ScreenData()

        if obj.exists('hex', from_tag) == False:
            raise TypeError('from_tag needs to be a vaild screen.hex')

        if obj.exists('hex', to_tag) == False:
            raise TypeError('to_tag needs to be a vaild screen.hex')

        if from_tag == to_tag:
            raise TypeError('to_tag and from_tag needs can not be the same')

        if self.rowExists(to_tag, from_tag):
            raise TypeError('this action already exists')

        row = {
            'from':from_tag,
            'too': to_tag
        }

        return super().create(row)


    def rowExists(self, to_hex, from_hex):
        obj = self.createObj()
        
        e = obj.tbl.contains(
            (Query().form == from_hex) and (Query().to == to_hex)
        )

        obj.close()
        return e

    def readActions(self, from_hex:str):

        obj = self.createObj()
        data = obj.tbl.search(Query()['from'] == from_hex)
        obj.close()

        return data

    def removeByHex(self, hex:str):

        obj = self.createObj()
        obj.tbl.remove(Query()['from']==hex)
        obj.tbl.remove(Query()['too']==hex)
        obj.close()

        return True
