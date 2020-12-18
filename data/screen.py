from string import digits, ascii_letters
from random import choices
from os.path import isfile

from tinydb_base import DatabaseBase
from tinydb import Query
import validators
import imghdr

from .commons import copylocalImg
from .exception import DataException

def _mkHex(l:int=8):
    pool = choices(population=(digits + ascii_letters), k=500)
    return ''.join(choices(population=pool, k=l))


class ScreenData(DatabaseBase):

    def __init__(self, file: str = 'ds.json', table: str = 'screenData', requiredKeys='hex,soundtrack,picture,title'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def _checkHex(self, hex:str):
        db = self.createObj()
        exists = db.tbl.contains(Query().hex == hex)
        db.close()

        return False

    def create(self, soundtrack:str, picture:str, title:str = 'screen') -> int:
        row = {}
        hexval = _mkHex()

        #makes a unique hex
        while self._checkHex(hexval) == True:
            hexval = _mkHex()

        row['hex'] = hexval

        #checks the url is vailid
        if validators.url(soundtrack) == False:
            raise TypeError('the sound track is not a valid url')

        row['soundtrack'] = soundtrack
        
        if isfile(picture) == False:
            raise TypeError('the picture needs to a local image')

        if imghdr.what(picture) == False:
            raise TypeError('the picture needs to a local image')

        row['picture'] = copylocalImg(picture)

        if isinstance(title, str) == False:
            raise TypeError('the title needs to be string')

        row['title'] = title


        return (super().create(row), row['hex'])

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

    def removeByHex(self, hex:str):
        db = self.createObj()
        if db.tbl.contains(Query().hex == hex) == False:
            raise DataException('the passed hex dose not exist')
        db.tbl.remove(Query().hex == hex)
        db.close()
        
        return True

    
