from tinydb.queries import Query
from .screen import ScreenData
from .history import History
from .actions import Actions
from .campain import CampainData
from .settings import SettingsData
from .combat import CombatData
from .players import Players
from .segment import Segment

import validators


class Screen(ScreenData):

    def update_title(self, hex:str, title:str):
        
        return self.update(
            hex=hex,
            tag='title',
            value=title
        )

    def update_soundtrack(self, hex:str, soundtrack:str):

        return self.update(
            hex=hex,
            tag='soundtrack',
            value=soundtrack
        )

    def update_picture(self, hex:str, picture:str):

        return self.update(
            hex=hex,
            tag='picture',
            value=picture
        )

    def update_dm_notes(self, hex:str, note:str):
    
        return self.update(
            hex=hex,
            tag='dm_notes',
            value=note
        )

    def update_pl_notes(self, hex:str, note:str):
        
        return self.update(
            hex=hex,
            tag='pl_notes',
            value=note
        )

    def readAll(self):
        setting = SettingsData().get('Active Campain')
        db = self.createObj()
        data = db.tbl.search(Query().campain == setting)
        data.sort(key=lambda x: x['title'], reverse=True)
        db.close()

        return data

    def readByHex(self, hex:str):

        db = self.createObj()
        row = db.tbl.get(Query().hex == hex)
        db.close()
        return row
    
class Settings(SettingsData): pass 

