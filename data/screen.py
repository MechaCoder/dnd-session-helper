from string import digits, ascii_lowercase
from random import choices
from os.path import isfile
from validators import url

from rich import print

from tinydb_base import DatabaseBase
from tinydb import Query
import validators
import imghdr

from .commons import copylocalImg
from .exception import DataException
from .settings import SettingsData

def _mkHex(l:int=8):
    pool = choices(population=(digits + ascii_lowercase), k=500)
    return ''.join(choices(population=pool, k=l))


class ScreenData(DatabaseBase):

    def __init__(self, file: str = 'ds.json', table: str = 'screenData', requiredKeys='hex,title,soundtrack,picture,dm_notes,pl_notes,campain:int'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)
        self.settings = SettingsData()

    def _checkHex(self, hex:str):
        db = self.createObj()
        exists = db.tbl.contains(Query().hex == hex)
        db.close()

        return False

    def create(self, soundtrack:str, picture:str, campain:int = 0, title:str = 'screen', dm_notes:str = '', pl_notes:str = ''):
        row = {}
        hexval = _mkHex(l=4)

        #makes a unique hex
        while self._checkHex(hexval) == True:
            hexval = _mkHex(l=4)

        row['hex'] = hexval

        #checks the url is vailid
        if validators.url(soundtrack) == False:
            raise TypeError('the sound track is not a valid url')

        row['soundtrack'] = soundtrack

        if isfile(picture) == False and url(picture) == False:
            raise TypeError('the picture needs to a local image or a url')

        row['picture'] = copylocalImg(picture)

        if isinstance(campain, int) == False:
            raise TypeError('the campain needs to a int')
        
        if campain == 0:
            campain = self.settings.get('Active Campain')

        row['campain'] = campain

        if isinstance(title, str) == False:
            raise TypeError('the title needs to be string')

        if title == None:
            title = ""

        row['title'] = str(title)

        if isinstance(dm_notes, str) == False:
            raise TypeError('the dm_notes need to be type string')
        
        if dm_notes == None:
            dm_notes = ""

        row['dm_notes'] = dm_notes

        if isinstance(pl_notes, str) == False:
            raise TypeError('the pl_notes need to be type string')

        if pl_notes == None:
            pl_notes = ""

        row['pl_notes'] = pl_notes

        created_id = super().create(row)
        return (created_id, row['hex'])

    def getByHex(self, hexval:str):
        
        db = self.createObj()
        row = db.tbl.get(Query().hex == hexval)
        db.close()
        return row

    def getListOfHexs(self):
        rows = []
        for row in self.readAll():
            rows.append(row['hex'])
        return rows

    def update(self, hex:str, tag:str, value:any):

        if isinstance(value, str) == False:
            return

        db = self.createObj()
        updated_ids = db.tbl.update({tag: value}, Query().hex == hex)
        db.close()
        return updated_ids

    def removeByHex(self, hex:str):
        db = self.createObj()
        if db.tbl.contains(Query().hex == hex) == False:
            raise DataException('the passed hex dose not exist')
        db.tbl.remove(Query().hex == hex)
        db.close()
        
        return True

    
