from tinydb.queries import Query
from tinydb_base import DatabaseBase

class NotesData(DatabaseBase):
    
    def __init__(self, file: str = 'ds.json', table: str = 'notesData', requiredKeys='screenid,text,private'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def create(self, screenid:int, text:str, private:bool = True):

        if isinstance(screenid, int) == False:
            raise TypeError('screenid should be an int')

        if isinstance(text, str) == False:
            raise TypeError('text should be an str')

        if isinstance(private, bool) == False:
            raise TypeError('private should be an bool')

        return super().create({
            'screenid': screenid,
            'text': text,
            'private': private
        })

    def readByScreenid(self, screenid, private:bool = False): 
        db = self.createObj()
        rows = db.tbl.search(
            (Query().screenid == screenid) & (Query().private == private)
        )
        db.close()
        return rows