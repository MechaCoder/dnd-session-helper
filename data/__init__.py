from .screen import ScreenData
from .settings import SettingsData

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
    

class Settings(SettingsData): pass 
