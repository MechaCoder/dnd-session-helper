from tinydb_base.getSet import GetSet, Factory, Query
from .base import BaseGetSet

class SettingsData(BaseGetSet):
    
    def __init__(self, table: str = 'settings'):
        super().__init__( table=table)

        if self.exist('Active Campain') == False:
            self.set('Active Campain', 1)

        if self.exist('chatHistory') == False:
            self.set('chatHistory', False)

        if self.exist('displayServerSide') == False:
            self.set('displayServerSide', True)

        if self.exist('screenTemplate') == False:
            self.set('screenTemplate', '')


    def exist(self, tag:str):
        db = Factory(self.fileName, self.tableName)
        exists = db.tbl.contains(Query().tag == tag)
        db.close()

        return exists

    def rmTag(self, tag:str):
        db = Factory(self.fileName, self.tableName)
        db.tbl.remove(Query().tag == tag)
        db.close()
        return True

    def readTags(self):
        db = Factory(self.fileName, self.tableName)
        
        tags = []
        for row in db.tbl.all():
            if row['tag'] == 'screenTemplate':
                continue
            
            tags.append(
                row['tag']
            )
        db.close()
        return tags

    def getAll(self):
        db = Factory(self.fileName, self.tableName)
        rows = db.tbl.all()
        db.close()

        return rows