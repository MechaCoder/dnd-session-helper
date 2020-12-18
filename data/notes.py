from tinydb.queries import Query
from tinydb_base import DatabaseBase

from os.path import isfile

from .commons import copylocalImg

class NotesData(DatabaseBase):
    
    def __init__(self, file: str = 'ds.json', table: str = 'notesData', requiredKeys='screenid,text,private,noteType'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)
        self._modual_update()

    def _modual_update(self):
        newColumns = {
            'noteType': 'text'
        }
        db = self.createObj()
        for row in db.tbl.all():
            newRow = {}
            doc_id = row.doc_id

            for key in row.keys():
                newRow[key] = row[key]
            
            for key in newColumns.keys():
                if key not in newRow.keys():
                    newRow[key] = newColumns[key]

            db.tbl.update(newRow, doc_ids=[doc_id])
        db.close()
        return True

    def create(self, screenid:int, text:str, private:bool = True, noteType:str='text'):

        if isinstance(screenid, int) == False:
            raise TypeError('screenid should be an int')

        if isinstance(text, str) == False:
            raise TypeError('text should be an str')

        if isinstance(private, bool) == False:
            raise TypeError('private should be an bool')

        if isinstance(noteType, str) == False:
            raise TypeError('the noteType should be a str')

        if noteType not in ['text', 'file']:
            raise TypeError('the note type is not a vaild type')

        if noteType == 'file':
            if isfile(text) == False:
                raise TypeError('if the the noteType is file the path has to be a file')

            text = copylocalImg(text)

        return super().create({
            'screenid': screenid,
            'text': text,
            'private': private,
            'noteType': noteType
        })

    def readByScreenid(self, screenid, private:bool = False): 
        db = self.createObj()
        rows = db.tbl.search(
            (Query().screenid == screenid) & (Query().private == private)
        )
        db.close()
        return rows