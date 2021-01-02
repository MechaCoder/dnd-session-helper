from typing import Type
from tinydb_base import DatabaseBase

class CampainData(DatabaseBase):

    def __init__(self, file: str = 'ds.json', table: str = 'campain', requiredKeys='title,bio'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

        if len(self.readAll()) == 0:
            self.create('my first campain')

    def create(self, title:str, bio:str = '') -> int:
        
        if isinstance(title, str) == False:
            raise TypeError('the title needs to a string')

        if isinstance(bio, str) == False:
            raise TypeError('the bio needs to be a string')
        
        row={
            'title': title,
            'bio': bio
        }
        
        return super().create(row)