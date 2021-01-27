from tinydb_base.getSet import GetSet, Factory, Query

class SettingsData(GetSet):
    
    def __init__(self, file: str = 'ds.json', table: str = 'settings'):
        super().__init__(file=file, table=table)

        if self.exist('Active Campain') == False:
            self.set('Active Campain', 1)

        if self.exist('chatH istory') == False:
            self.set('chatHistory', False)

        if self.exist('displayServerSide'):
            self.set('displayServerSide', False)


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