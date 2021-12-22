from faker import Faker

from .base import BaseData
from .screen import ScreenData
from tinydb import Query
from .api import MonstersIndex

class CombatData(BaseData):

    def __init__(self, table: str = 'combatData', requiredKeys='screen.hex:str,title:str,notes:str'):
        super().__init__(table=table, requiredKeys=requiredKeys)

    def create(self, screenHex:str, title:str, notes:str):

        screenObj = ScreenData()

        if screenObj.exists('hex', screenHex) is False:
            raise Exception('the screen must be vaild.')
        
        row = {
            'screen.hex': screenHex,
            'title': title,
            'notes': notes
        }
        return super().create(row)

    def readByHex(self, hex: str):
        obj = self.createObj()
        data = obj.tbl.search(Query()['screen.hex'] == hex)
        obj.close()
        return data


class NpcData(BaseData):

    def __init__(self, table: str = "npcData", requiredKeys='name:str,index:str,conditions:str,combat.id:int'):
        super().__init__(table=table, requiredKeys=requiredKeys)

    def create(self, name:str, index:str, combat_id:int):

        if str(combat_id) not in CombatData().readDoc_ids():
            raise Exception('the combat id must exist')

        if MonstersIndex().exists('index', index) is False:
            raise Exception('this monster dose not exists')
        row = {
            'name': name,
            'index': index,
            'conditions': "",
            'combat.id': int(combat_id)
        }

        return super().create(row)

    def readByHex(self, combat_id:int):

        obj = self.createObj()
        data = obj.tbl.search(Query()['combat.id'] == combat_id)
        obj.close()

        return data
