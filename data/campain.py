from tinydb_base import DatabaseBase
from .base import BaseData

class CampainData(BaseData):

    def __init__(self, table: str = 'campain', requiredKeys='title,bio'):
        super().__init__(table=table, requiredKeys=requiredKeys)

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