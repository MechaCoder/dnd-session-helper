from tinydb.queries import Query
from .screen import ScreenData
from .settings import SettingsData
from .campain import CampainData
from .combat import EncounterData
from .history import History
from .actions import Actions

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

    def readAll(self) -> list:
        setting = SettingsData().get('Active Campain')
        db = self.createObj()
        data = db.tbl.search(Query().campain == setting)
        db.close()

        return data

    
class Settings(SettingsData): pass 

class Campain(CampainData):

    def listDoc_ids(self):

        ids = []
        for row in self.readAll():
            ids.append(
                str(row.doc_id)
            )
        return ids

class Combat(EncounterData): 

    def create(self, name: str, url: str) -> int:

        if validators.url(url) == False:
            raise TypeError('url is not vaild url')

        campaign_id = Settings().get('Active Campain')
        return super().create(name, url, campaign_id)
